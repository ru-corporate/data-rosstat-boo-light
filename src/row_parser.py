from collections import OrderedDict
from inspect_columns import Columns
from numpy import int64 


INT_TYPE = int64
EMPTY = int('0')
QUOTE_CHAR = '"'


# transform numbers
def rub_to_thousand(x: int):
    return int(round(0.001*float(x)))


def mln_to_thousand(x: int):
    return 1000*int(x)


# transform strings
def okved3(code_string: str):
    """Get 3 levels of OKVED codes from *code_string*."""
    codes = [int(x) for x in code_string.split(".")]
    return codes + [EMPTY] * (3-len(codes))


def dequote(name: str):
    """Split company *name* to organisation and title."""
    # Warning: will not work well on company names with more than 4 quotechars
    parts = name.split(QUOTE_CHAR)
    org = parts[0].strip()
    cnt = name.count(QUOTE_CHAR)
    if cnt == 2:
        title = parts[1].strip()
    elif cnt > 2:
        title = QUOTE_CHAR.join(parts[1:])
    else:
        title = name
    return org, title.strip()    

# TODO: make exclusions list    
# Exclusions 1 (values do not change between 2015 and 2013):
#ex1 = ['7733574312', '7703200101', '7726725828', '7116503278', '7720531939', '7802084784', '5261047820', '7717716979', '7707635583', '7707635618', '7707631814', '7707631780', '7707631807', '7707631797', '7707669230', '7707627840', '7710662717', '7707622136', '7707620724', '7707627776', '7710658157', '5906001179']
# Exclusions 2 (values not present in 2013):
#ex2 = ['6950089368', '7611020211', '7610052884', '8905049712', '2815015806', '6213008693', '1121012228', '1118005125', '1323126443', '7325134560', '6518008962', '7206025330', '2130035819', '7718000240', '5709000962', '7206045664', '1648030286', '4027094050', '2815006255', '2315097141', '2815014640', '6901077218', '6950086060', '3905069565', '3702549950', '7716239258', '7303018465', '2304030498', '1637001364', '7702845690', '7725261651', '6164029105', '6168079234', '6168084403', '7717795579', '7717536373', '7715801523', '4205301359', '4813012497', '5014010858', '1841013578', '4253006177', '5014011210', '5001101970', '5047117229', '3327846679', '2466134701', '2463256170', '7722347452', '7721160109', '7717045174', '7719592060', '6452117213', '6732039141', '4501092289', '2805005661', '7701681463', '6732110676', '6027165441', '3123322170', '2805003992', '2130152872', '7328077286', '7705506286', '5836140137', '7733561183', '2815000253', '6674188744', '7723683376', '3905049865', '6658444790', '2505006167', '7325037091', '4401126706', '1101029209', '7729781193', '6450942683', '3849003247', '7734549284', '6731079744', '7743929349', '5446014200', '7841345694', '2309112930', '6453123474', '7810414570', '3827041432', '7805304212', '2815005879', '7736049488', '4028057910', '7724892421', '3702037215', '7804011894', '5906088532', '7718622498', '1435120070', '6615000704', '1106020457', '6679065810', '7728260046', '4401145321', '7721692512', '2368006719', '2815015193', '2466202366', '7713791982', '7731293958', '7203315506', '6729041327', '4501165314', '3661054152', '3702654754', '5609174620', '2463223230', '7309901211', '7708231417', '3525335891', '7723624437', '2315983686', '6732004163', '3904070663', '3827034234', '7327058629', '5079011747', '5406755700', '4725001320', '2315096155', '5027112060', '6729019593', '7725253964', '3815015340', '5260398223', '6673243664', '5037009337', '3905069572', '7802803904', '7707785130', '9102015605', '6729018590', '7810593094', '6450046006', '5054009672', '3906262040', '7327026602', '6123023584', '7802510023', '7810804186', '7701996223', '6321360609', '6729019995', '5037003085', '5027229990', '7802877416', '7204009117', '5754003450', '7728011057', '7720292769', '7804528900', '7810345292', '5403196147', '7017273506', '7839477358', '6685035122', '7728509565', '6727051030', '7720719497', '6679060184', '2456007655', '7725563170', '7723361964', '7718107899', '3906206800', '7328001262', '3917017346', '6234143069', '7842511986', '6732031985', '2225145841', '6658460960', '7328073500', '7816477545', '7701414450', '7715230774', '7811451582', '7714774806', '6732067935', '7718590736', '6375190390', '7805286556', '1323124196', '2320222239', '5017099124', '7714002609', '7733259470', '7726263605', '7718036775', '6903006974', '1903022374', '2310127748', '6316151342', '7537011867', '1660028580', '6674336128', '7810895507', '7430008090', '9102173947', '7715030800', '7736527247', '7802178023', '5012052098', '7727224052', '3816006147', '7727180599', '7536102568', '1903005308', '7841323147', '7729747675', '6732073897', '7708256796', '2713015927', '3816006073', '5260380868', '7709736890', '7717535683', '5029160870', '6684004410', '7725844484', '7714775863', '7726080841', '7732115027', '7709864878', '7715556695', '7715789185', '3665073332', '7708091985', '4217103094', '6679054462', '7701385351', '5040087261', '5018151391', '4501107908', '7743689129', '7710062967', '7813229022', '7719065391', '7627024620', '6672181694', '7733005250', '7721762030', '4703044256', '6658425758', '6678006314', '7804069580', '6623071096', '6678003095', '6672339162', '1645030136', '7715441398', '5047121112', '7724589129', '6316133544', '2330029989', '7729642249']

#UNIT385_EXCLUSIONS = ex1 + ex2   


def get_unit_adjuster(unit_name: str):
    _mapper = {'383': rub_to_thousand,
               '385': mln_to_thousand,
               '384': lambda x: x}
    if unit_name in _mapper.keys():
        return _mapper[unit_name]
    else:
        raise ValueError(f"Unit not supported: {unit_name}")
    

def parse_row_to_list(rowd: OrderedDict, datacols = Columns.DATACOLS) -> []:
    """Return modified *rowd* as list."""
    # assemble new text columns
    ok1, ok2, ok3 = okved3(rowd['okved'])
    org, title = dequote(rowd['name'])
    region = rowd['inn'][0:2]    
    # warning: 'date' may not be in rowd.keys() in some early datasets
    date_reviewed = rowd['date']
    # text    
    text = [date_reviewed, ok1, ok2, ok3,
            org, title, region, rowd['inn'],
            rowd['okpo'], rowd['okopf'], rowd['okfs'],
            rowd['unit']]
    # adjust values to '000 rub 
    unit = rowd['unit']
    func = get_unit_adjuster(unit)
    data = [func(rowd[k]) for k in datacols]
    return text + data


def get_parsed_colnames(renamed_datacols = Columns.RENAMED_DATACOLS):
    """Return colnames corresponding to parse_row()."""
    return ['date', 'ok1', 'ok2', 'ok3',
            'org', 'title', 'region', 'inn',
            'okpo', 'okopf', 'okfs',
            'unit'] + renamed_datacols


def get_colname_dtypes():
    """Return types correspoding to get_colnames().
       Used to speed up CSV import in custom_df_reader(). """
    dtype_dict = {k: INT_TYPE for k in get_parsed_colnames()}
    string_cols = ['date', 'org', 'title', 'region', 'inn',
                   'okpo', 'okopf', 'okfs']
    dtype_dict.update({k: str for k in string_cols})
    return dtype_dict

COLNAMES = get_parsed_colnames()
DTYPES = get_colname_dtypes()

def parse_row_to_dict(rowd, colnames = COLNAMES):
    row = parse_row_to_list(rowd) 
    return OrderedDict(zip(colnames, row))