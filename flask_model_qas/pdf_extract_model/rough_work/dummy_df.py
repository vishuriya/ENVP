import pandas as pd
df_list = [['SI \nNo. \n \nKind \nDescription  of  Goods \nHSN/SAC   \nQuantity', 'Rate', 'per', 'Amount', 'CGST %', 'SGST %'], ['No. \nof  Pkgs.', '', '', '', '9', '9'], ['1 \n \n80X25 \n  Hydrochloric  Acid \n28061000  \n2,000.00  kg', '5.25', 'kg', '10,500.00', '9', '9'], ['Kgs', '', '', '', '9', '9'], ['30%', '', '', '', '9', '9'], ['CGST.-9%', '91%', '', '945.00', '9', '9'], ['prme \nSGST -  9% \na%  ', '9', '%', '945.00', '9', '9'], ['ibaa  BATE  TF \n', '', '', '', '9', '9'], ['oy \nt', '', '', '', '9', '9'], ['none \n \nTOOPTSe', '', '', '', '9', '9'], ['', '', '', '', '9', '9'], [' \n', '', '', '', '9', '9'], ['GORE', '', '', '', '9', '9'], ['Mts', '', '', '', '9', '9'], ['ee \nee', '', '', '', '9', '9'], [' \nTotal \n2,000.00  kg', '', '', '  12,390.00', '9', '9'], ['Amount  Chargeable  in  words', '', '', 'E. \n  O.E', '9', '9'], ['Indian  Rupees  Twelve  Thousand  Three  Hundred  Ninety  Only', '', '', '', '9', '9']]
df_list_2 = [['jLaxmi  Organic  Industries  Ltd. \n \nUnit-2  ', 'he', 'te \ncae', 'Terms  of  Delivery', 'Cuan \n \nRate \nper, \nAmount \n'], ['Plot \nNo. \nB \n#  2/2, \n3/1/1, \n3', '', '', '', ''], ['/1/2,  MIDC ,  Mahad,  Dist.-  Raigad- \n402301', '', '', '', ''], ['GSTIN/UIN \n:  27AAACL2435R1Z5', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], [' \n', '', '', '', ''], [' \nSI \nNo. \n \nKind \n \nDescription \nof  Goods', '', '', 'HSN/SAG', 'Cuan \n \nRate \nper, \nAmount \n'], [' \nT', '', '', '', ''], ['f \n46 \nHDPE/PP  LAMINATED  BAGS', '', '', '3923', ' \n5,110.00 \npes. \n16.15 \npcs \n50,226.50'], [' \n \nSize:-  537.5  x  900    Printed  ', '', '', '', ' \n \n \n \n'], ['', '', '', '', ' \n \n'], ['Without  Extra  Polythene  Bag \nhet', '', '', '', ''], [' \n \nProduct  :-  AASP  CYAN  BAND', '', '', '', ''], ['15  Bundles x  200  Bags  3000  Bags', '', '', '', ' \n \n \n'], ['01  Bundle  x \n110  Bags  \n110  Bags', '', '', '', ' \n'], ['TCS  Category  for  Sales \nof \nAny  Goods \n \n0.075%', '', '', '', ' \n \n \n'], ['', '', '', 'ee', ' \n \nee'], ['', 'C-GST  TAX', '', '9%  S', ' \n \n9  % \n \n4,520.39'], ['', 'S-GST  TAX  9%  S', '', '', ' \n9% \n \n4,520.39'], ['', 'TCS  on  Sales  0.1% ', '', '', ' \n196. \n \n59.00'], ['', '', '', '', ' \n59,326.28'], ['Less \n:', '', '', 'Round  Off', ' \n \n-0.28'], ['', '', '', '', 'es \n'], ['', '', '', '', 'Oe \n'], ['', '', '', '', ''], ['', '', '', 'i', '4 \n'], ['', '', '', 'he', ' \n'], ['', '', '', '', ''], ['', '', '', '', ' \n'], ['', '', '', 'on \na', ' \n'], ['', '', '', '', ''], ['', '', '', '', ' \n'], [' \n', '', '', '', ' \n'], ['ae \n', '', '', '', ' \n \n'], ['', '', '', '', 'pe \n'], ['', '', '', '1', ' \n'], ['', '', '', '', ' \n'], ['', '', '', '', ' \n'], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ' \n \nae \n'], ['', '', '', '', 'Pray'], ['', '', '', '', ' \nbeg \n'], [' \n \n', '', '', '', ' \n \n \n'], [' \n \n', '', '', '', ' \n \n \n'], [' \n', '', '', '', ' \n \n'], [' \n', '', '', '', ' \n \n'], ['ft', '', '', '', ' \neo \nbr'], ['', '', '', '', ' \n \na'], [' \nae \n', '', '', '', ' \n'], ['We \n', '', '', '', ' \n \n \n'], ['iver', '', '', 'cs \n:', ' \naes \n'], ['ees \n3', '', '', 'Total', ' \n3,110.00  pos \n    59,326.00 '], ['', '', '', '', 'E2OE'], [' \nChargeable  in  words \nAmount \n', '', '', '', ''], ['IRs \nFifty  Nine  Thousand  Three  Hundred  Twenty  Six  Only', '', '', '', 'ee \n'], ['', '', '', 'Value \nRate', 'Amount    Rate Amount    Tax  Amount'], ['', '', '', '9% \n50,226.50', '9%   4,520.39  9,040.78 \n4,520.39'], ['3923', '', '', '', ''], ['', '', '', 'Total  60,226.60,', '4,620.39 \n  4,620.39 \n9,040.78'], ['  Tax  Amount  in  ee', 'Rs  Nine  Thousand  Forty  and  Seventy  Eight  piste  Only', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']]
df = pd.DataFrame(df_list)

print(df)