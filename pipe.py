from eos_cloud.tools import p2cor, cor2xml, crop, fusion, automl_prep

if __name__ == "__main__":
    argv1 = ['--img_dir=e:/Data/EOS/new/imgs',
    '--label_dir=e:/Data/EOS/new/labels',
    '--dst=e:/Data/EOS/new/ret/'
    ]
    # p2cor.main(argv1)
    argv2 = ['--input=e:/Data/EOS/new/ret/points.json',
    '--output=e:/Data/EOS/new/ret/raw_xml']
    # cor2xml.main(argv2)
    argv3 = ['--img_dir=e:/Data/EOS/new/imgs',
    '--img_dst=e:/Data/EOS/new/ret/tmp',
    '--xml_dir=e:/Data/EOS/new/ret/raw_xml',
    '--xml_dst=e:/Data/EOS/new/ret/tmp_xml']
    argv4 = ['--img_dir=e:/Data/EOS/imgs',
    '--img_dst=e:/Data/EOS/ret/tmp',
    '--xml_dir=e:/Data/EOS/xml_adjust',
    '--xml_dst=e:/Data/EOS/ret/tmp_xml']
    # crop.main(argv3)
    # crop.main(argv4)
    argv5 = ['--img_dir=e:/Data/EOS/new/ret/tmp',
    '--img_dst=e:/Data/EOS/fusion/imgs',
    '--xml_dir=e:/Data/EOS/new/ret/tmp_xml',
    '--xml_dst=e:/Data/EOS/fusion/xmls']
    argv6 = ['--img_dir=e:/Data/EOS/ret/tmp',
    '--img_dst=e:/Data/EOS/fusion/imgs',
    '--xml_dir=e:/Data/EOS/ret/tmp_xml',
    '--xml_dst=e:/Data/EOS/fusion/xmls']
    # fusion.main(argv5)
    # fusion.main(argv6)
    argv7 = ['--xml_dir=e:/Data/EOS/fusion/xmls',
    '--dst=e:/Data/EOS/automl']
    # automl_prep.main(argv7)