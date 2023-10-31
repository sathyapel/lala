from distutils.log import debug
from encodings import normalize_encoding
from simple_ddl_parser import DDLParser
import pprint

results = DDLParser(
"""
# Create some veyr simple orders
CREATE TABLE orders (
  order_date DATE NOT NULL,
  purchaser INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
) AUTO_INCREMENT = 10001;


""", normalize_names=True).run(group_by_type=True)

pprint.pprint(results) 
