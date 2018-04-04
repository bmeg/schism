import os.path
import commands
import tempfile

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("schism")

def write_temp_file(body):
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(body)
    temp.close()
    return temp

class ConvertHandler(tornado.web.RequestHandler):
    def post(self):
        from_build = self.get_arguments('from')[0]
        to_build = self.get_arguments('to')[0]
        chain = "chains/hg%sToHg%s.over.chain.gz" % (from_build, to_build)
        print("converting from hg%s to hg%s using %s chain file" % (from_build, to_build, chain))
        if os.path.isfile(chain):
            bed = self.request.files['bed'][0]
            filename = bed['filename']
            temp = write_temp_file(bed['body'])
            out = tempfile.NamedTemporaryFile(delete=False)
            crossmap = commands.getoutput("Crossmap.py bed %s %s %s" % (chain, temp.name, out.name))
            data = out.read()
            self.write(data)
        else:
            error = "chain file does not exist for converting from hg%s to hg%s" % (from_build, to_build)
            self.write(error)

        self.finish()

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/convert", ConvertHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(7771)
    tornado.ioloop.IOLoop.current().start()
