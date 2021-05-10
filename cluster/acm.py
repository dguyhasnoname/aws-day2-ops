from modules.get_acm import _ACM
from modules.output import Output

class ACM():
    def get_acm():
        certs = _ACM.get_acm()
        header = ['DomainName', 'ARN', 'Status', 'RenewalEligibility', 'IssuedAt']
        Output.print_table(certs, header, True)

def main():
    ACM.get_acm()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[ERROR] Interrupted from keyboard!")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0) 