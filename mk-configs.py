import json

with open('/usr/local/etc/xray/config.json') as json_file:
    config_data = json.load(json_file)

    configs = []

    inbounds = config_data['inbounds']

    for i in range(1, len(inbounds)):
        inbound = config_data['inbounds'][i]
        clients = inbound['settings']['clients']
        protocol = inbound['protocol']
        port = inbound['port']
        type = inbound['streamSettings']['network']
        security = inbound['streamSettings']['security']
        if security == 'tls' and type == 'ws':
           alpn = inbound['streamSettings']['tlsSettings']['alpn']
           sni = inbound['streamSettings']['tlsSettings']['serverName']
           fingerprint = inbound['streamSettings']['tlsSettings']['settings']['fingerprint']
           path = inbound['streamSettings']['wsSettings']['path']
           host = inbound['streamSettings']['wsSettings']['headers']['host']
           serviceName = ''
           reslvAlpn = ','.join(alpn)
           url = f"&fp={fingerprint}&alpn={reslvAlpn}&sni={sni}&path={path}&host={host}"
        elif security == 'tls' and type == 'grpc':
           alpn = inbound['streamSettings']['tlsSettings']['alpn']
           sni = inbound['streamSettings']['tlsSettings']['serverName']
           fingerprint = inbound['streamSettings']['tlsSettings']['settings']['fingerprint']
           serviceName = inbound['streamSettings']['grpcSettings']['serviceName']
           path=''
           host=''
           reslvAlpn = ','.join(alpn)
           url = f"&fp={fingerprint}&alpn={reslvAlpn}&sni={sni}&serviceName={serviceName}"
        elif security == 'reality' and type == 'grpc':
           alpn = ''
           path=''
           host=''
           sni = inbound['streamSettings']['realitySettings']['serverName']
           dest = inbound['streamSettings']['realitySettings']['dest']
           serverNames = inbound['streamSettings']['realitySettings']['serverNames']
           privateKey = inbound['streamSettings']['realitySettings']['privateKey']
           pbk = inbound['streamSettings']['realitySettings']['publicKey']
           sid = inbound['streamSettings']['realitySettings']['shortIds']
           fingerprint = inbound['streamSettings']['realitySettings']['fingerprint']
           spx = inbound['streamSettings']['realitySettings']['spiderX']
           serviceName = inbound['streamSettings']['grpcSettings']['serviceName']
           reslvSid = ','.join(sid)
           url = f"&fp={fingerprint}&dest={dest}&serviceName={serviceName}&sni={serverNames[1]}&spx={spx}&sid={reslvSid}&pbk={pbk}"
        else:
            protocol = ''
            port = ''
            type = ''
            security = ''
            alpn = ''
            sni = ''
            fingerprint = ''
            path = ''
            host = ''
            serviceName = ''
            dest = ''
            serverNames = ''
            privateKey = ''
            publicKey = ''
            sid = ''
            spx = ''
        for j in range(len(clients)):
            user = clients[j]["email"]
            if protocol == 'trojan':
               uuid = clients[j]["password"]
            else:
               uuid = clients[j]["id"]
            config = f"{protocol}://{uuid}@{sni}:{port}?type={type}&security={security}{url}#{user}"
            configs.append(config)


config_str = '\n'.join(configs)

with open('/var/www/html/v2rayConfig.txt', 'w'):
     pass
print("Rewrited the Config!")

with open('/var/www/html/v2rayConfig.txt', 'a') as mixConfigs:
    mixConfigs.write(config_str)
print("Created the Config!")
