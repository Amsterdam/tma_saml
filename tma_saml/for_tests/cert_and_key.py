"""
    Generated fixtures for certificate and private key.
    Expected expiration: April 25th, 2020

    When these expire the tests based on this fixtures will fail,
    in that case, new fixtures are required:

    `
    $ openssl genrsa -out server.pem 2048

    $ openssl req -new -key server.pem -out server.csr

    # With the following specs:
    #     Country Name (2 letter code) [AU]:NL
    #     State or Province Name (full name) [Some-State]:.
    #     Locality Name (eg, city) []:Amsterdam
    #     Organization Name (eg, company) [Internet Widgits Pty Ltd]:.
    #     Organizational Unit Name (eg, section) []:Datapunt
    #     Common Name (e.g. server FQDN or YOUR name) []:brp.api-acc.datapunt.amsterdam.nl
    #     Email Address []:.
    #
    #     Please enter the following 'extra' attributes
    #     to be sent with your certificate request
    #     A challenge password []:.
    #     An optional company name []:.

    $ openssl x509 -req -days 1185 -in server.csr -signkey server.pem -out server.crt
    `

    paste the content of the files server.crt and server.pem in the fixtures below and delete the files.

"""

server_crt = """-----BEGIN CERTIFICATE-----
MIIDPDCCAiQCCQDDcGbre8lk+zANBgkqhkiG9w0BAQUFADBgMQswCQYDVQQGEwJO
TDESMBAGA1UEBxMJQW1zdGVyZGFtMREwDwYDVQQLEwhEYXRhcHVudDEqMCgGA1UE
AxMhYnJwLmFwaS1hY2MuZGF0YXB1bnQuYW1zdGVyZGFtLm5sMB4XDTE3MDEyNTEy
MjcwMloXDTIwMDQyNDEyMjcwMlowYDELMAkGA1UEBhMCTkwxEjAQBgNVBAcTCUFt
c3RlcmRhbTERMA8GA1UECxMIRGF0YXB1bnQxKjAoBgNVBAMTIWJycC5hcGktYWNj
LmRhdGFwdW50LmFtc3RlcmRhbS5ubDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCC
AQoCggEBAK9JN9v3fTElYbG8Ukyp83ZiT7EyfntXIomDqs+un+7pTAiNaX6goadI
yYk5xUPWDiNOOaAK2JhsOkfA91NWKdiDAxljQmGkBvFa3eqqdPqmxr6JcgbYRdKF
62pEwjCVeoQJOBKtQmKp6RL+DxwU01U51+bb85daHR/XTZrfz+23bCm6b8TaVDle
5nyL/vLfgGioass6/s+wH5w/i1Yt4FgUw+y6FlF4PbBggjhdtJFbnH41azykcOxm
kfVMek/7Qo3kE5sjkMkY1ZtyTKr5cHbjCz6X7bgbO2u3QUNmU6+gway8qB2z0j47
djNjRz2lpvWJ/JCH9LfIfAAQUd06FUkCAwEAATANBgkqhkiG9w0BAQUFAAOCAQEA
LZhlw7QDn1z2D1tlgzg6jTrFwd2HlSX7NnYgqhuagiNUDFhrZWQPGoKsSv2mlYzl
8gJEWoWCE9Aiy4s3hAqlOESMG2zCfeJNcudZIsOsVRjIcUw0do+IUz9mebu44Bsc
nnhK7x1rbjJza8rH98i18nAGdJJAiXr6/M8bWXZw36FF1KVsDZyXmmKTw95JBQUT
9MRvRTNOusQcpsMcyO0gEFZ6ZgscNSwhhtwHNqahcZ3U7XA/fWzFIhUPOflf3QvX
gwXOpHJD4iqc0OigTmufEErIWA6tL/l0tkUNvqpO2SZzRmCCTgfrcmisPEitkcer
X1NZeoRknv7kr25EH7GWkw==
-----END CERTIFICATE-----
"""
server_pem = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAr0k32/d9MSVhsbxSTKnzdmJPsTJ+e1ciiYOqz66f7ulMCI1p
fqChp0jJiTnFQ9YOI045oArYmGw6R8D3U1Yp2IMDGWNCYaQG8Vrd6qp0+qbGvoly
BthF0oXrakTCMJV6hAk4Eq1CYqnpEv4PHBTTVTnX5tvzl1odH9dNmt/P7bdsKbpv
xNpUOV7mfIv+8t+AaKhqyzr+z7AfnD+LVi3gWBTD7LoWUXg9sGCCOF20kVucfjVr
PKRw7GaR9Ux6T/tCjeQTmyOQyRjVm3JMqvlwduMLPpftuBs7a7dBQ2ZTr6DBrLyo
HbPSPjt2M2NHPaWm9Yn8kIf0t8h8ABBR3ToVSQIDAQABAoIBAQCkZ9tBsK62kuY/
y2+xwlG9PtaaT878Jq0ZJ+rlIleVwTH0b5Z8E3OrsIR+9jWEu9fE25EHAEVJKXG8
bUxM2OskzTTx8fyIEk4EwIKWoMxZcGXGvqm5q85JeBxnLxiocvtXrkHump1CZzVZ
//ryDsJtFHThbnnaAsaAX/PFCJlAzxMyp5FuH42wPqqTIfnFvKXjNo3Bbby+1boS
Or7g5mMoy5PsMgh+6/ZSWOWy9Y3uDTCZxzD0ZFHwyeK6hJgUoD/+k7fvFBi3n5Xh
YuqayV/NZ4FymB3S+FfT9QxzxenPL4xBUlzt8x4KOkpbUQG7SRkiXH7lDCZPTZww
jtHrKK41AoGBAOj6aekYSCLzOMOO+36z6eyiBBqOiIUSjG9j42PIIX35dXNZVeRi
8F0cpeQUvAE5/k1cEP96Y1V2KyqVHeblJyYzMkyzLXdL1VLT/Ub3yvgSF0bo5kXY
EV5u11DU8Y+lsRdAoeg74ubSfG8FXDNSb1bJEPr+WJvNv4PPrb32cF07AoGBAMCb
YZWW1NY41TvUXrEITd3GYb2l5T0E7sa2wVgDPN+lsJuWTX2JtbRhRdB4XqhcT8ia
9xwvg5yr1i242ergBqnZyA9m4na/GAiP2uQRKYlto/g8Hb6ih4RrheabkQ7upcg2
grMNswikpaqwBepocxhhqE7IRqFz/KcErj+VQ/9LAoGAXJzO5T4lzt7ovbRk/ST/
5HUzNGtckamh8dW/Wrb/uVgk/EmS/0rlSd5Ng7FKWyJ2mMH0b9pzClIDLtZAIL0P
JvxLDnpbpISctGRY1pFCOgLXBfUnNLSDkwp0xUkhDX1MPHYQ5oSH2kHp/SggUrZ+
U/1xppTdHHJZo0g3RMBmQmkCgYBf/lERc/4Z0nN8ASk8hE4CpTfbhE4PLmEvCrCs
A9kYAgVWVf/C/JpiD0TzVLqgoHlnGszj8E5hDEePvBxn8kV/67nI61cdJbp9sey/
VEpmYw2gz51ngKuX9Nrkh04xqgFYGsrjIIXFXgHvYxFftbT/RtTShwCkwSD/wNZz
fBpKpwKBgGsKcARjraEWLEhVFITI/VCX3tTdN3FTFAGDY1n956hptYz3emjih6Qs
uL/JsuXaqkMRwMegMzboYaNtxbHUJ+lPf00k49Po2X+5zAz0li4h+7aWpWS3aOHv
0dkr8+M8i2Xnpr1ZtFYQZ/lbOvzkorHdlRIL1nltZE2eXQqvTVWN
-----END RSA PRIVATE KEY-----
""".encode('utf-8')

secondary_server_crt = """-----BEGIN CERTIFICATE-----
MIIDizCCAnMCFG9MduB1QeE8j4vIBlZtKJoPdKjWMA0GCSqGSIb3DQEBCwUAMIGB
MQswCQYDVQQGEwJOTDETMBEGA1UECAwKU29tZS1TdGF0ZTESMBAGA1UEBwwJQW1z
dGVyZGFtMQowCAYDVQQKDAEsMREwDwYDVQQLDAhEYXRhcHVudDEqMCgGA1UEAwwh
YnJwLmFwaS1hY2MuZGF0YXB1bnQuYW1zdGVyZGFtLm5sMB4XDTE5MDYxNzE0NTMz
MFoXDTIyMDkxNDE0NTMzMFowgYExCzAJBgNVBAYTAk5MMRMwEQYDVQQIDApTb21l
LVN0YXRlMRIwEAYDVQQHDAlBbXN0ZXJkYW0xCjAIBgNVBAoMASwxETAPBgNVBAsM
CERhdGFwdW50MSowKAYDVQQDDCFicnAuYXBpLWFjYy5kYXRhcHVudC5hbXN0ZXJk
YW0ubmwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCjuJeqb+jRwfXq
EO3n0S8J7Fa7cjnCmw7CndoHxRcXRVhyKuj3X/Hg+xZXFSEupaS6zH/tZYkmgI0a
Uk5PzToeCpJsBY9nwqaK9vAKlBcMyA/Cq+vU2p8FOGvULZrv8ppgKHEjdDWWfGpu
m19s37f1jkcwq53jj7UTDHE/wPqaVP/OqHTILv8/edrGdr2zx4waACm94CTN4l/r
LZWw3cVm6ef20je0yumDSVWmGU0DE2UJ3N8TDs8az13LQLCQxyloFnlVU/4p5uZT
7zZeMdkZxWd4gWtumJjbA2KAowhtEZNKhRyDgPnRdTmHMdxmnCXphbofh4dfYm/V
kR9p3dxdAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAHb3GaFQt2cbhAJL0cciIC1d
7zlYc+lP979Tk++zGulwasdr0Qlr9MTSDo0Jsy+4IweWjqjMAbMvMjlwB9eGf2x5
Y90ops9LQLqUsTXBnWNLdx1664rMDb0kP35POb45YRKubQfyXaGMe3V/M2i0zfv7
GwWgxVSuPkQiQm61HWaOIkZb6ORwGiNrWeMHEcgV30mVkuXfWb3Okfz3q/7Okqlt
mnvn8eNXciR2VYR6cai+vLFAv2wUa1F5v/FtUWLAhS9Z6McR5jt/3SEUoksfWgky
vUa1cqki4SXB3D1euAaD0/nJIybmma9klaxraTRkYQjyuZ6GyYH2b07Y2zD0IDE=
-----END CERTIFICATE-----
"""
secondary_server_pem = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAo7iXqm/o0cH16hDt59EvCexWu3I5wpsOwp3aB8UXF0VYciro
91/x4PsWVxUhLqWkusx/7WWJJoCNGlJOT806HgqSbAWPZ8KmivbwCpQXDMgPwqvr
1NqfBThr1C2a7/KaYChxI3Q1lnxqbptfbN+39Y5HMKud44+1EwxxP8D6mlT/zqh0
yC7/P3naxna9s8eMGgApveAkzeJf6y2VsN3FZunn9tI3tMrpg0lVphlNAxNlCdzf
Ew7PGs9dy0CwkMcpaBZ5VVP+KebmU+82XjHZGcVneIFrbpiY2wNigKMIbRGTSoUc
g4D50XU5hzHcZpwl6YW6H4eHX2Jv1ZEfad3cXQIDAQABAoIBAAbqNP2t3Fd/qbNJ
I8M2wpXYtZEVMftWMTlnEV5ipKcG9sVbqptIIh8ue7MR4WTm+h4ppP2R3EkUBOGn
uEcGk/3Q1H5bfcMUJZSY+Wp49sBDcub1++/xi+XcjDFZ+8FGrd6B1sV4kwrYFma1
iUI/8LUeXUNg/DowR6WWUPIwZGVAQH7EXMRSUScb8I0AzxtcBWHty1mrjEq7KuBS
RronODxlUcYR7aj5pP7RA4csuH9uQXYfdO8vlaRY/YP83lJrUZ6UeXdYyPmrJnKX
kimDGXFB4uu39GX3DPz8GyG2U9vtxlJF8tdt7P+EkCDTLGU+G4Of5qELC2TuZvlK
yv2ZfAECgYEA1UYrqz8YDYijir4jlj5w1QXt/M+UJic4eIo1cDHdLCMYJQ58Qi79
PjhpjjQXQKEy7HWAfI1Bh8PSdmj9oAqiJNTtpRB7o7z1eCvGUiThJZCaJaor5kBx
PE13bLqqtlt+CdZMektg1xi8AbYzU/qgvPQIh+tr1MSGlBfffN8TtpECgYEAxIUU
Iv+OTJaNGHQ44MioCKfBCjSwEU6q3XAHxaQvuvcY9aVnXw6/DyJdV7STGJOQeyJV
cXIlnkhRFA5vPnZ0jUcgr6lC3eXnD6kVNv2jS4yPfrKxQU2mWThb21baNb6O47cn
4hd/6T888z+r7ESJZdbWg4DmwWekAYDcJvH1pw0CgYEAww20LqA7vVT0TZXsMiLV
St5rdEXctrA0I3ozuXLBVvaZxHplBpq3Hcq2L0pQ4dkMG9qzMjZ2claUC5umKlLP
TGQ5HDfg/DV7Qva2ILZ9+78uW7gxAhp59a7bxGNMcg9nTFPkCg0ael6yw9YBR5L2
oxmFG9oh+qvqcVMMIMZc3yECgYBuSGhWg6etn0crE/3fV3vE769LNOohrE4C2p3h
8hO/Dm/5Wos6MyJRMe3EDFgIELeiAlCEy5QE0Xx+juMq4Hrj1aioK4qU0DHs/ewj
4g7DlOvqJAmJJjRWGWSjIIhwZLH3ZI+DN8DWemCP+YlXm9anSfsz7SCSJMFK/q+N
Q3eh+QKBgFZfEWpYaSY6EIXg86P9GS0ZD/4BKT50waA99oRYyMPVDzcwZi21UQLV
XWUlqtNw7tpD7HbhnqhjOV6DdfZ6dtVCOkydCN+IkqCum6205GN9RO5uvXabJ/+6
YsICJZlzZr2fbDDphRmhWScL2fgaOy574IMNq+3qYzf59hldKWqU
-----END RSA PRIVATE KEY-----
""".encode('utf-8')
