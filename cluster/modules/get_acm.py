class _ACM:
    def get_acm(session):
        # session = Login.aws_session()
        acm_client = session.client("acm")
        list_of_acm = acm_client.list_certificates(CertificateStatuses=["ISSUED"])
        certs = list_of_acm.get("CertificateSummaryList")
        cluster_acm_list = []
        for cert_info in certs:
            cert_arn = cert_info.get("CertificateArn")

            cert_details = acm_client.describe_certificate(CertificateArn=cert_arn)
            cert = cert_details.get("Certificate")
            if cert["InUseBy"]:
                cluster_acm_list.append(
                    [
                        cert_info.get("DomainName"),
                        cert_arn,
                        cert["Status"],
                        cert["RenewalEligibility"],
                        cert["IssuedAt"],
                        cert_info.get("SubjectAlternativeNames"),
                    ]
                )

        return cluster_acm_list
