from python_terraform import Terraform


def deploy():
    print("Deploy")
    t = Terraform("src/terraform")
    t.init()


deploy()
