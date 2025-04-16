import os, shutil

dst = "./public"
source = "./static"


def copy_to_public():
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    def rec(path=""):
        parent=os.path.join(source, path)
        for item in os.listdir(parent):
            source_path = os.path.join(source, path, item)
            dst_path = os.path.join(dst, path, item)
            if os.path.isfile(source_path):
                shutil.copy(source_path, dst_path)
                print(f"copying {source_path} to {dst_path}")
            else:
                os.mkdir(dst_path)
                print(f"mkdir: {dst_path}")
                rec(os.path.join(path,item))

    rec()
