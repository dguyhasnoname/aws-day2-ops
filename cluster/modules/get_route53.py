
class GetRoute53():
    # def get_route53(session):
    #     global route53_client
    #     route53_client = session.client('route53')
    #     route53_list = route53_client.list_hosted_zones()
    #     route53_details, zone_id = [], ''
    #     for zone in route53_list['HostedZones']:
    #         print(zone)
    #         print("\n")
    #         zone_id = zone['Id'].split('/')[-1]
    #         dns_struct = [zone_id, zone['Name'], str(zone['ResourceRecordSetCount']), str(zone['Config']['PrivateZone'])]
    #         route53_details.append(dns_struct)
    #     return route53_details

    def get_zone_record(paginator, zone_id):
        zone_records = paginator.paginate(HostedZoneId=zone_id)
        
        for record_set in zone_records:
            res_records = ''
            for record in record_set['ResourceRecordSets']:
                temp_res_records = []
                if any(record['Type'] in s for s in ['CNAME', 'A', 'NS']):
                    try:
                        for x in record['ResourceRecords']:
                            temp_res_records.append(x['Value'])                                        
                    except:
                        temp_res_records.append(record['AliasTarget']['DNSName'])

                    res_records = res_records + record['Name'] + '\n' + str(temp_res_records) + '\n'
        res_records = res_records.rstrip('\n')
        return res_records

    def get_route53_hosted_zones(session, cluster):
        route53_client = session.client('route53')
        route53_list = route53_client.list_hosted_zones()
        paginator = route53_client.get_paginator('list_resource_record_sets')
        cluster_route53_records, all_route53_records  = [], []
        zone_id, zone_name, zone_record_count, zone_pvt = [''] * 4

        for zone in route53_list['HostedZones']:
            zone_id = zone['Id'].split('/')[-1]
            zone_name = zone['Name']
            zone_record_count = str(zone['ResourceRecordSetCount'])
            zone_pvt = str(zone['Config']['PrivateZone'])

            if cluster:
                if cluster in zone_name:
                    res_records = GetRoute53.get_zone_record(paginator, zone_id)
                    dns_struct = [zone_id, zone_name, zone_record_count, zone_pvt, res_records]
                    cluster_route53_records.append(dns_struct)
            else:
                res_records = GetRoute53.get_zone_record(paginator, zone_id)
                dns_struct = [zone_id, zone_name, zone_record_count, zone_pvt, res_records]
                all_route53_records.append(dns_struct)

        if cluster:
            return cluster_route53_records
        else:
            return all_route53_records