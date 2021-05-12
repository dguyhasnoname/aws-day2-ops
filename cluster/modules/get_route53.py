
class _Route53():
    def get_route53(session):
        global route53_client
        route53_client = session.client('route53')
        route53_list = route53_client.list_hosted_zones()
        route53_details = []
        for zone in route53_list['HostedZones']:
            zone_id = zone['Id'].split('/')[-1]
            route53_details.append([zone_id, zone['Name'], zone['ResourceRecordSetCount'], zone['Config']['PrivateZone']])
        
        return route53_details

    def get_route53_hosted_zones(session, cluster, verbose):
        route53_details = _Route53.get_route53(session)
        paginator = route53_client.get_paginator('list_resource_record_sets')
        route53_records = []
        for x in route53_details:
            zone_records = paginator.paginate(HostedZoneId=x[0])
            if cluster in x[1]:
                for record_set in zone_records:
                    for record in record_set['ResourceRecordSets']:
                        if record['Type'] == 'CNAME' or record['Type'] == 'A':
                            try:
                                route53_records.append([record['Name'], record['AliasTarget']['DNSName']])
                            except KeyError:
                                route53_records.append([record['Name'], record['ResourceRecords'][0]['Value']])
        return route53_records
        
