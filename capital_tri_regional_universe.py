# ==============================================================================
# ANGKOR QUANT: CAPITAL.COM TRI-REGIONAL INSTITUTIONAL UNIVERSE (AQ89)
# Invariant 89: Top 100 US, Top 100 EU, Top 100 ASIA RAM Memory & Kill Zone Routing
# ==============================================================================
# Author: Angkor Quant AI Architecture Team (Founder: HEM SINATH)
# Standard: Nanosecond RAM Ingestion (< 0.0001ms), Tri-Regional Market Hours,
#           Dual-Directional (Buy-Sell) Institutional Confluence & Dynamic Capital Slots.
# ==============================================================================

import time
import datetime
from typing import Dict, List, Tuple, Any, Optional, Set

# ------------------------------------------------------------------------------
# 1. TOP 100 US INSTITUTIONAL UNIVERSE (S&P 100, NASDAQ 100 & LIQUID LEADERS)
# ------------------------------------------------------------------------------
TOP_100_US_DATA: List[Dict[str, str]] = [
    {"epic": "US100", "name": "Nasdaq 100 Tech Index", "sector": "Index", "type": "INDEX"},
    {"epic": "US500", "name": "S&P 500 Large-Cap Index", "sector": "Index", "type": "INDEX"},
    {"epic": "US30", "name": "Dow Jones Industrial Average", "sector": "Index", "type": "INDEX"},
    {"epic": "US2000", "name": "Russell 2000 Small-Cap Index", "sector": "Index", "type": "INDEX"},
    {"epic": "NVDA", "name": "Nvidia Corporation", "sector": "Semiconductors", "type": "EQUITY"},
    {"epic": "AAPL", "name": "Apple Inc", "sector": "Consumer Electronics", "type": "EQUITY"},
    {"epic": "MSFT", "name": "Microsoft Corporation", "sector": "Cloud & Software", "type": "EQUITY"},
    {"epic": "AMZN", "name": "Amazon.com Inc", "sector": "E-Commerce & Cloud", "type": "EQUITY"},
    {"epic": "GOOGL", "name": "Alphabet Inc (Google)", "sector": "Internet & Search", "type": "EQUITY"},
    {"epic": "META", "name": "Meta Platforms Inc", "sector": "Social Media & VR", "type": "EQUITY"},
    {"epic": "TSLA", "name": "Tesla Inc", "sector": "EV & Autonomous", "type": "EQUITY"},
    {"epic": "AVGO", "name": "Broadcom Inc", "sector": "Semiconductors", "type": "EQUITY"},
    {"epic": "AMD", "name": "Advanced Micro Devices", "sector": "Semiconductors", "type": "EQUITY"},
    {"epic": "NFLX", "name": "Netflix Inc", "sector": "Streaming Entertainment", "type": "EQUITY"},
    {"epic": "INTC", "name": "Intel Corporation", "sector": "Semiconductors", "type": "EQUITY"},
    {"epic": "QCOM", "name": "Qualcomm Inc", "sector": "Wireless & Chips", "type": "EQUITY"},
    {"epic": "TXN", "name": "Texas Instruments Inc", "sector": "Analog Chips", "type": "EQUITY"},
    {"epic": "MU", "name": "Micron Technology", "sector": "Memory Chips", "type": "EQUITY"},
    {"epic": "AMAT", "name": "Applied Materials", "sector": "Semiconductor Equipment", "type": "EQUITY"},
    {"epic": "LRCX", "name": "Lam Research Corp", "sector": "Semiconductor Equipment", "type": "EQUITY"},
    {"epic": "ADI", "name": "Analog Devices", "sector": "Semiconductors", "type": "EQUITY"},
    {"epic": "PANW", "name": "Palo Alto Networks", "sector": "Cybersecurity", "type": "EQUITY"},
    {"epic": "CRWD", "name": "CrowdStrike Holdings", "sector": "Cybersecurity", "type": "EQUITY"},
    {"epic": "CRM", "name": "Salesforce Inc", "sector": "Enterprise Software", "type": "EQUITY"},
    {"epic": "ADBE", "name": "Adobe Inc", "sector": "Creative Software", "type": "EQUITY"},
    {"epic": "ORCL", "name": "Oracle Corporation", "sector": "Database & Cloud", "type": "EQUITY"},
    {"epic": "NOW", "name": "ServiceNow Inc", "sector": "Workflow Cloud", "type": "EQUITY"},
    {"epic": "CSCO", "name": "Cisco Systems", "sector": "Networking", "type": "EQUITY"},
    {"epic": "IBM", "name": "International Business Machines", "sector": "Enterprise Tech & AI", "type": "EQUITY"},
    {"epic": "V", "name": "Visa Inc", "sector": "Payments", "type": "EQUITY"},
    {"epic": "MA", "name": "Mastercard Inc", "sector": "Payments", "type": "EQUITY"},
    {"epic": "JPM", "name": "JPMorgan Chase & Co", "sector": "Banking & Finance", "type": "EQUITY"},
    {"epic": "BAC", "name": "Bank of America Corp", "sector": "Banking", "type": "EQUITY"},
    {"epic": "WFC", "name": "Wells Fargo & Co", "sector": "Banking", "type": "EQUITY"},
    {"epic": "C", "name": "Citigroup Inc", "sector": "Banking", "type": "EQUITY"},
    {"epic": "GS", "name": "Goldman Sachs Group", "sector": "Investment Banking", "type": "EQUITY"},
    {"epic": "MS", "name": "Morgan Stanley", "sector": "Wealth & Investment", "type": "EQUITY"},
    {"epic": "BLK", "name": "BlackRock Inc", "sector": "Asset Management", "type": "EQUITY"},
    {"epic": "SCHW", "name": "Charles Schwab Corp", "sector": "Brokerage & Finance", "type": "EQUITY"},
    {"epic": "AXP", "name": "American Express Co", "sector": "Consumer Finance", "type": "EQUITY"},
    {"epic": "PGR", "name": "Progressive Corp", "sector": "Insurance", "type": "EQUITY"},
    {"epic": "CB", "name": "Chubb Limited", "sector": "Insurance", "type": "EQUITY"},
    {"epic": "LLY", "name": "Eli Lilly and Co", "sector": "Pharmaceuticals", "type": "EQUITY"},
    {"epic": "UNH", "name": "UnitedHealth Group", "sector": "Healthcare Services", "type": "EQUITY"},
    {"epic": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare & Pharma", "type": "EQUITY"},
    {"epic": "ABBV", "name": "AbbVie Inc", "sector": "Biopharmaceuticals", "type": "EQUITY"},
    {"epic": "MRK", "name": "Merck & Co Inc", "sector": "Pharmaceuticals", "type": "EQUITY"},
    {"epic": "PFE", "name": "Pfizer Inc", "sector": "Pharmaceuticals", "type": "EQUITY"},
    {"epic": "TMO", "name": "Thermo Fisher Scientific", "sector": "Life Sciences", "type": "EQUITY"},
    {"epic": "ABT", "name": "Abbott Laboratories", "sector": "Medical Devices", "type": "EQUITY"},
    {"epic": "DHR", "name": "Danaher Corp", "sector": "Diagnostics & Research", "type": "EQUITY"},
    {"epic": "BMY", "name": "Bristol-Myers Squibb", "sector": "Biopharma", "type": "EQUITY"},
    {"epic": "AMGN", "name": "Amgen Inc", "sector": "Biotechnology", "type": "EQUITY"},
    {"epic": "GILD", "name": "Gilead Sciences", "sector": "Biopharma", "type": "EQUITY"},
    {"epic": "ISRG", "name": "Intuitive Surgical", "sector": "Robotic Surgery", "type": "EQUITY"},
    {"epic": "VRTX", "name": "Vertex Pharmaceuticals", "sector": "Biotech", "type": "EQUITY"},
    {"epic": "REGN", "name": "Regeneron Pharmaceuticals", "sector": "Biotech", "type": "EQUITY"},
    {"epic": "SYK", "name": "Stryker Corp", "sector": "Medical Tech", "type": "EQUITY"},
    {"epic": "MDT", "name": "Medtronic plc", "sector": "Medical Devices", "type": "EQUITY"},
    {"epic": "COST", "name": "Costco Wholesale Corp", "sector": "Retail Wholesale", "type": "EQUITY"},
    {"epic": "WMT", "name": "Walmart Inc", "sector": "Retail Supercenters", "type": "EQUITY"},
    {"epic": "TGT", "name": "Target Corp", "sector": "Discount Retail", "type": "EQUITY"},
    {"epic": "HD", "name": "Home Depot Inc", "sector": "Home Improvement", "type": "EQUITY"},
    {"epic": "LOW", "name": "Lowe's Companies Inc", "sector": "Home Improvement", "type": "EQUITY"},
    {"epic": "MCD", "name": "McDonald's Corp", "sector": "Fast Food", "type": "EQUITY"},
    {"epic": "SBUX", "name": "Starbucks Corp", "sector": "Coffee & Beverage", "type": "EQUITY"},
    {"epic": "NKE", "name": "Nike Inc", "sector": "Sportswear", "type": "EQUITY"},
    {"epic": "DIS", "name": "Walt Disney Co", "sector": "Media & Entertainment", "type": "EQUITY"},
    {"epic": "CMG", "name": "Chipotle Mexican Grill", "sector": "Restaurants", "type": "EQUITY"},
    {"epic": "PG", "name": "Procter & Gamble Co", "sector": "Consumer Goods", "type": "EQUITY"},
    {"epic": "KO", "name": "Coca-Cola Co", "sector": "Beverages", "type": "EQUITY"},
    {"epic": "PEP", "name": "PepsiCo Inc", "sector": "Beverages & Snacks", "type": "EQUITY"},
    {"epic": "MDLZ", "name": "Mondelez International", "sector": "Confectionery", "type": "EQUITY"},
    {"epic": "CL", "name": "Colgate-Palmolive Co", "sector": "Consumer Staples", "type": "EQUITY"},
    {"epic": "CAT", "name": "Caterpillar Inc", "sector": "Heavy Machinery", "type": "EQUITY"},
    {"epic": "DE", "name": "Deere & Co", "sector": "Agricultural Equipment", "type": "EQUITY"},
    {"epic": "BA", "name": "Boeing Co", "sector": "Aerospace & Defense", "type": "EQUITY"},
    {"epic": "GE", "name": "General Electric Co", "sector": "Aviation & Energy", "type": "EQUITY"},
    {"epic": "HON", "name": "Honeywell International", "sector": "Industrial Conglomerate", "type": "EQUITY"},
    {"epic": "UNP", "name": "Union Pacific Corp", "sector": "Railroads", "type": "EQUITY"},
    {"epic": "UPS", "name": "United Parcel Service", "sector": "Logistics & Freight", "type": "EQUITY"},
    {"epic": "RTX", "name": "RTX Corporation", "sector": "Aerospace & Defense", "type": "EQUITY"},
    {"epic": "LMT", "name": "Lockheed Martin Corp", "sector": "Defense Technology", "type": "EQUITY"},
    {"epic": "GD", "name": "General Dynamics", "sector": "Defense & Marine", "type": "EQUITY"},
    {"epic": "ETN", "name": "Eaton Corporation", "sector": "Power Management", "type": "EQUITY"},
    {"epic": "XOM", "name": "Exxon Mobil Corp", "sector": "Integrated Oil & Gas", "type": "EQUITY"},
    {"epic": "CVX", "name": "Chevron Corp", "sector": "Energy & Oil", "type": "EQUITY"},
    {"epic": "COP", "name": "ConocoPhillips", "sector": "Oil Exploration", "type": "EQUITY"},
    {"epic": "SLB", "name": "Schlumberger Ltd", "sector": "Oilfield Services", "type": "EQUITY"},
    {"epic": "EOG", "name": "EOG Resources", "sector": "Shale Oil & Gas", "type": "EQUITY"},
    {"epic": "NEE", "name": "NextEra Energy", "sector": "Clean Utilities", "type": "EQUITY"},
    {"epic": "SO", "name": "Southern Company", "sector": "Electric Utilities", "type": "EQUITY"},
    {"epic": "DUK", "name": "Duke Energy Corp", "sector": "Utilities", "type": "EQUITY"},
    {"epic": "LIN", "name": "Linde plc", "sector": "Industrial Gases", "type": "EQUITY"},
    {"epic": "SHW", "name": "Sherwin-Williams Co", "sector": "Specialty Coatings", "type": "EQUITY"},
    {"epic": "APD", "name": "Air Products & Chemicals", "sector": "Industrial Gases", "type": "EQUITY"},
    {"epic": "FCX", "name": "Freeport-McMoRan Inc", "sector": "Copper Mining", "type": "EQUITY"},
    {"epic": "NEM", "name": "Newmont Corporation", "sector": "Gold Mining", "type": "EQUITY"},
    {"epic": "PLTR", "name": "Palantir Technologies", "sector": "Defense AI & Analytics", "type": "EQUITY"},
    {"epic": "GOLD", "name": "Spot Gold / US Dollar", "sector": "Precious Metals", "type": "COMMODITY"},
]

# ------------------------------------------------------------------------------
# 2. TOP 100 EUROPEAN INSTITUTIONAL UNIVERSE (DAX 40, FTSE 100, CAC 40, EURO STOXX)
# ------------------------------------------------------------------------------
TOP_100_EU_DATA: List[Dict[str, str]] = [
    {"epic": "DE40", "name": "German DAX 40 Index", "sector": "Index", "type": "INDEX"},
    {"epic": "UK100", "name": "UK FTSE 100 Index", "sector": "Index", "type": "INDEX"},
    {"epic": "FR40", "name": "France CAC 40 Index", "sector": "Index", "type": "INDEX"},
    {"epic": "EU50", "name": "Euro Stoxx 50 Index", "sector": "Index", "type": "INDEX"},
    {"epic": "SWI20", "name": "Swiss SMI 20 Index", "sector": "Index", "type": "INDEX"},
    {"epic": "IT40", "name": "Italy FTSE MIB Index", "sector": "Index", "type": "INDEX"},
    {"epic": "ES35", "name": "Spain IBEX 35 Index", "sector": "Index", "type": "INDEX"},
    {"epic": "NL25", "name": "Netherlands AEX Index", "sector": "Index", "type": "INDEX"},
    {"epic": "ASML", "name": "ASML Holding NV", "sector": "Lithography Equipment", "type": "EQUITY"},
    {"epic": "SAP", "name": "SAP SE", "sector": "Enterprise Software", "type": "EQUITY"},
    {"epic": "MC", "name": "LVMH Moët Hennessy", "sector": "Luxury Goods", "type": "EQUITY"},
    {"epic": "NOVO_B", "name": "Novo Nordisk A/S", "sector": "Pharmaceuticals", "type": "EQUITY"},
    {"epic": "NESN", "name": "Nestlé SA", "sector": "Food & Beverage", "type": "EQUITY"},
    {"epic": "ROG", "name": "Roche Holding AG", "sector": "Healthcare & Diagnostics", "type": "EQUITY"},
    {"epic": "NOVBN", "name": "Novartis AG", "sector": "Pharmaceuticals", "type": "EQUITY"},
    {"epic": "SIE", "name": "Siemens AG", "sector": "Industrial Engineering", "type": "EQUITY"},
    {"epic": "AIR", "name": "Airbus SE", "sector": "Aerospace & Commercial Jets", "type": "EQUITY"},
    {"epic": "TTE", "name": "TotalEnergies SE", "sector": "Integrated Energy", "type": "EQUITY"},
    {"epic": "SAN", "name": "Sanofi SA", "sector": "Pharmaceuticals", "type": "EQUITY"},
    {"epic": "SU", "name": "Schneider Electric SE", "sector": "Energy Management", "type": "EQUITY"},
    {"epic": "AI", "name": "Air Liquide SA", "sector": "Industrial Gases", "type": "EQUITY"},
    {"epic": "RMS", "name": "Hermès International", "sector": "Ultra Luxury", "type": "EQUITY"},
    {"epic": "OR", "name": "L'Oréal SA", "sector": "Cosmetics & Beauty", "type": "EQUITY"},
    {"epic": "CDG", "name": "Christian Dior SE", "sector": "Luxury Fashion", "type": "EQUITY"},
    {"epic": "BNP", "name": "BNP Paribas SA", "sector": "European Banking", "type": "EQUITY"},
    {"epic": "CS", "name": "AXA SA", "sector": "Insurance & Asset Management", "type": "EQUITY"},
    {"epic": "DTE", "name": "Deutsche Telekom AG", "sector": "Telecommunications", "type": "EQUITY"},
    {"epic": "ALV", "name": "Allianz SE", "sector": "Insurance & Financials", "type": "EQUITY"},
    {"epic": "BAYN", "name": "Bayer AG", "sector": "Crop Science & Pharma", "type": "EQUITY"},
    {"epic": "BAS", "name": "BASF SE", "sector": "Chemicals", "type": "EQUITY"},
    {"epic": "BMW", "name": "Bayerische Motoren Werke AG", "sector": "Luxury Automotive", "type": "EQUITY"},
    {"epic": "MBG", "name": "Mercedes-Benz Group AG", "sector": "Luxury Automotive", "type": "EQUITY"},
    {"epic": "VOW3", "name": "Volkswagen AG", "sector": "Automotive Group", "type": "EQUITY"},
    {"epic": "DHL", "name": "Deutsche Post DHL", "sector": "Global Logistics", "type": "EQUITY"},
    {"epic": "ADS", "name": "Adidas AG", "sector": "Sporting Apparel", "type": "EQUITY"},
    {"epic": "IFX", "name": "Infineon Technologies AG", "sector": "Power Semis", "type": "EQUITY"},
    {"epic": "MUV2", "name": "Munich Re Group", "sector": "Reinsurance", "type": "EQUITY"},
    {"epic": "RWE", "name": "RWE AG", "sector": "Renewables & Utilities", "type": "EQUITY"},
    {"epic": "ENEL", "name": "Enel SpA", "sector": "Electric Utilities", "type": "EQUITY"},
    {"epic": "ENI", "name": "Eni SpA", "sector": "Oil & Gas", "type": "EQUITY"},
    {"epic": "ISP", "name": "Intesa Sanpaolo SpA", "sector": "Italian Banking", "type": "EQUITY"},
    {"epic": "BBVA", "name": "Banco Bilbao Vizcaya Argentaria", "sector": "Banking", "type": "EQUITY"},
    {"epic": "SAN_MC", "name": "Banco Santander SA", "sector": "Global Banking", "type": "EQUITY"},
    {"epic": "IBE", "name": "Iberdrola SA", "sector": "Renewable Power", "type": "EQUITY"},
    {"epic": "ITX", "name": "Inditex (Zara)", "sector": "Fast Fashion Retail", "type": "EQUITY"},
    {"epic": "AZN", "name": "AstraZeneca plc", "sector": "Oncology & Vaccines", "type": "EQUITY"},
    {"epic": "SHEL", "name": "Shell plc", "sector": "Global Energy", "type": "EQUITY"},
    {"epic": "HSBA", "name": "HSBC Holdings plc", "sector": "Global Banking", "type": "EQUITY"},
    {"epic": "ULVR", "name": "Unilever plc", "sector": "Consumer Products", "type": "EQUITY"},
    {"epic": "BP", "name": "BP plc", "sector": "Energy & Oil", "type": "EQUITY"},
    {"epic": "GSK", "name": "GSK plc", "sector": "Pharmaceuticals", "type": "EQUITY"},
    {"epic": "RELX", "name": "RELX Group plc", "sector": "Analytics & Publishing", "type": "EQUITY"},
    {"epic": "DGE", "name": "Diageo plc", "sector": "Premium Beverages", "type": "EQUITY"},
    {"epic": "BATS", "name": "British American Tobacco", "sector": "Tobacco & Nicotine", "type": "EQUITY"},
    {"epic": "BARC", "name": "Barclays plc", "sector": "Investment Banking", "type": "EQUITY"},
    {"epic": "LLOY", "name": "Lloyds Banking Group", "sector": "Retail Banking", "type": "EQUITY"},
    {"epic": "VOD", "name": "Vodafone Group plc", "sector": "Telecoms", "type": "EQUITY"},
    {"epic": "PRU", "name": "Prudential plc", "sector": "Life Insurance", "type": "EQUITY"},
    {"epic": "RIO", "name": "Rio Tinto plc", "sector": "Mining & Iron Ore", "type": "EQUITY"},
    {"epic": "GLEN", "name": "Glencore plc", "sector": "Commodity Trading & Mining", "type": "EQUITY"},
    {"epic": "AAL", "name": "Anglo American plc", "sector": "Diversified Mining", "type": "EQUITY"},
    {"epic": "CRH", "name": "CRH plc", "sector": "Building Materials", "type": "EQUITY"},
    {"epic": "FLTR", "name": "Flutter Entertainment", "sector": "Online Gaming", "type": "EQUITY"},
    {"epic": "EXPN", "name": "Experian plc", "sector": "Credit Information", "type": "EQUITY"},
    {"epic": "NG", "name": "National Grid plc", "sector": "Power Grid", "type": "EQUITY"},
    {"epic": "HEIA", "name": "Heineken NV", "sector": "Brewing", "type": "EQUITY"},
    {"epic": "INGA", "name": "ING Groep NV", "sector": "Digital Banking", "type": "EQUITY"},
    {"epic": "ADYEN", "name": "Adyen NV", "sector": "Fintech Payments", "type": "EQUITY"},
    {"epic": "STLA", "name": "Stellantis NV", "sector": "Automotive", "type": "EQUITY"},
    {"epic": "STM", "name": "STMicroelectronics NV", "sector": "Automotive Chips", "type": "EQUITY"},
    {"epic": "RACE", "name": "Ferrari NV", "sector": "Supercars & Luxury", "type": "EQUITY"},
    {"epic": "PRY", "name": "Prysmian SpA", "sector": "Energy Cables", "type": "EQUITY"},
    {"epic": "SAF", "name": "Safran SA", "sector": "Aerospace Engines", "type": "EQUITY"},
    {"epic": "EL", "name": "EssilorLuxottica", "sector": "Eyewear & Optics", "type": "EQUITY"},
    {"epic": "KER", "name": "Kering SA", "sector": "Luxury Brands (Gucci)", "type": "EQUITY"},
    {"epic": "RI", "name": "Pernod Ricard SA", "sector": "Spirits & Wine", "type": "EQUITY"},
    {"epic": "BN", "name": "Danone SA", "sector": "Dairy & Nutrition", "type": "EQUITY"},
    {"epic": "CAP", "name": "Capgemini SE", "sector": "IT Consulting", "type": "EQUITY"},
    {"epic": "DSY", "name": "Dassault Systèmes SE", "sector": "3D Software", "type": "EQUITY"},
    {"epic": "CON", "name": "Continental AG", "sector": "Tires & Auto Parts", "type": "EQUITY"},
    {"epic": "HEN3", "name": "Henkel AG & Co KGaA", "sector": "Adhesives & Consumer", "type": "EQUITY"},
    {"epic": "FME", "name": "Fresenius Medical Care", "sector": "Dialysis & Care", "type": "EQUITY"},
    {"epic": "MRK_DE", "name": "Merck KGaA", "sector": "Science & Tech", "type": "EQUITY"},
    {"epic": "VNA", "name": "Vonovia SE", "sector": "Residential Real Estate", "type": "EQUITY"},
    {"epic": "SY1", "name": "Symrise AG", "sector": "Flavors & Fragrances", "type": "EQUITY"},
    {"epic": "BEI", "name": "Beiersdorf AG", "sector": "Skincare (Nivea)", "type": "EQUITY"},
    {"epic": "QIA", "name": "Qiagen NV", "sector": "Molecular Diagnostics", "type": "EQUITY"},
    {"epic": "ZAL", "name": "Zalando SE", "sector": "E-Commerce Fashion", "type": "EQUITY"},
    {"epic": "P911", "name": "Porsche AG", "sector": "Sports Cars", "type": "EQUITY"},
    {"epic": "SRT3", "name": "Sartorius AG", "sector": "Bioprocess Solutions", "type": "EQUITY"},
    {"epic": "UCG", "name": "UniCredit SpA", "sector": "Pan-European Banking", "type": "EQUITY"},
    {"epic": "ISP_MI", "name": "Intesa Sanpaolo Milan", "sector": "Banking", "type": "EQUITY"},
    {"epic": "TIT", "name": "Telecom Italia SpA", "sector": "Telecommunications", "type": "EQUITY"},
    {"epic": "G", "name": "Assicurazioni Generali", "sector": "Insurance", "type": "EQUITY"},
    {"epic": "REP", "name": "Repsol SA", "sector": "Oil & Gas", "type": "EQUITY"},
    {"epic": "TEF", "name": "Telefónica SA", "sector": "Telecoms", "type": "EQUITY"},
    {"epic": "AMS", "name": "Amadeus IT Group", "sector": "Travel Tech", "type": "EQUITY"},
    {"epic": "SILVER", "name": "Spot Silver / US Dollar", "sector": "Precious Metals", "type": "COMMODITY"},
    {"epic": "OIL_CRUDE", "name": "US WTI Crude Oil", "sector": "Commodity", "type": "COMMODITY"},
    {"epic": "OIL_BRENT", "name": "Brent Crude Oil", "sector": "Commodity", "type": "COMMODITY"},
]

# ------------------------------------------------------------------------------
# 3. TOP 100 ASIAN INSTITUTIONAL UNIVERSE (NIKKEI 225, HANG SENG, ASX 200, TOKYO)
# ------------------------------------------------------------------------------
TOP_100_ASIA_DATA: List[Dict[str, str]] = [
    {"epic": "JP225", "name": "Nikkei 225 Index (Japan)", "sector": "Index", "type": "INDEX"},
    {"epic": "HK50", "name": "Hang Seng Index (Hong Kong)", "sector": "Index", "type": "INDEX"},
    {"epic": "CN50", "name": "China A50 Index", "sector": "Index", "type": "INDEX"},
    {"epic": "AUS200", "name": "ASX 200 Index (Australia)", "sector": "Index", "type": "INDEX"},
    {"epic": "SG30", "name": "Straits Times Index (Singapore)", "sector": "Index", "type": "INDEX"},
    {"epic": "TW30", "name": "Taiwan Capitalization Weighted Index", "sector": "Index", "type": "INDEX"},
    {"epic": "7203", "name": "Toyota Motor Corp", "sector": "Automotive Leader", "type": "EQUITY"},
    {"epic": "6758", "name": "Sony Group Corp", "sector": "Entertainment & Sensor Tech", "type": "EQUITY"},
    {"epic": "6861", "name": "Keyence Corp", "sector": "Industrial Sensors & Factory Auto", "type": "EQUITY"},
    {"epic": "8035", "name": "Tokyo Electron Ltd", "sector": "Semiconductor Equipment", "type": "EQUITY"},
    {"epic": "8306", "name": "Mitsubishi UFJ Financial", "sector": "Mega Banking", "type": "EQUITY"},
    {"epic": "9984", "name": "SoftBank Group Corp", "sector": "Tech Investment & Vision", "type": "EQUITY"},
    {"epic": "9983", "name": "Fast Retailing (Uniqlo)", "sector": "Apparel Giant", "type": "EQUITY"},
    {"epic": "4063", "name": "Shin-Etsu Chemical Co", "sector": "Silicon Wafers & Chemicals", "type": "EQUITY"},
    {"epic": "6501", "name": "Hitachi Ltd", "sector": "Industrial Digital Solutions", "type": "EQUITY"},
    {"epic": "7974", "name": "Nintendo Co Ltd", "sector": "Video Games & IP", "type": "EQUITY"},
    {"epic": "7267", "name": "Honda Motor Co Ltd", "sector": "Automotive & Power Products", "type": "EQUITY"},
    {"epic": "8316", "name": "Sumitomo Mitsui Financial", "sector": "Banking & Brokerage", "type": "EQUITY"},
    {"epic": "6098", "name": "Recruit Holdings Co", "sector": "HR Tech & Indeed", "type": "EQUITY"},
    {"epic": "4568", "name": "Daiichi Sankyo Co", "sector": "Oncology Pharmaceuticals", "type": "EQUITY"},
    {"epic": "4502", "name": "Takeda Pharmaceutical", "sector": "Biopharma Global", "type": "EQUITY"},
    {"epic": "6981", "name": "Murata Manufacturing", "sector": "Electronic Components (MLCC)", "type": "EQUITY"},
    {"epic": "7741", "name": "Hoya Corporation", "sector": "Optical Glasses & Mask Blanks", "type": "EQUITY"},
    {"epic": "6273", "name": "SMC Corporation", "sector": "Pneumatic Control Equipment", "type": "EQUITY"},
    {"epic": "8001", "name": "Itochu Corporation", "sector": "Trading Conglomerate", "type": "EQUITY"},
    {"epic": "8002", "name": "Marubeni Corporation", "sector": "General Trading", "type": "EQUITY"},
    {"epic": "8058", "name": "Mitsubishi Corporation", "sector": "Global Energy & Materials", "type": "EQUITY"},
    {"epic": "8031", "name": "Mitsui & Co Ltd", "sector": "Trading & Resources", "type": "EQUITY"},
    {"epic": "6902", "name": "Denso Corporation", "sector": "Automotive Components", "type": "EQUITY"},
    {"epic": "8411", "name": "Mizuho Financial Group", "sector": "Banking & Securities", "type": "EQUITY"},
    {"epic": "9433", "name": "KDDI Corporation", "sector": "Mobile Telecoms", "type": "EQUITY"},
    {"epic": "9432", "name": "Nippon Telegraph & Telephone", "sector": "Telecom Infrastructure", "type": "EQUITY"},
    {"epic": "6954", "name": "Fanuc Corporation", "sector": "Industrial Robots & CNC", "type": "EQUITY"},
    {"epic": "7733", "name": "Olympus Corporation", "sector": "Medical Endoscopes", "type": "EQUITY"},
    {"epic": "6301", "name": "Komatsu Ltd", "sector": "Construction & Mining Equipment", "type": "EQUITY"},
    {"epic": "6326", "name": "Kubota Corporation", "sector": "Farm Machinery & Engines", "type": "EQUITY"},
    {"epic": "7751", "name": "Canon Inc", "sector": "Optics, Printers & Medical", "type": "EQUITY"},
    {"epic": "5108", "name": "Bridgestone Corp", "sector": "Tires & Rubber", "type": "EQUITY"},
    {"epic": "6752", "name": "Panasonic Holdings", "sector": "Batteries & Electronics", "type": "EQUITY"},
    {"epic": "6971", "name": "Kyocera Corporation", "sector": "Ceramic Components", "type": "EQUITY"},
    {"epic": "0700", "name": "Tencent Holdings", "sector": "Internet & Gaming Leader", "type": "EQUITY"},
    {"epic": "9988", "name": "Alibaba Group Holding", "sector": "E-Commerce & Cloud", "type": "EQUITY"},
    {"epic": "3690", "name": "Meituan", "sector": "On-Demand Delivery Platform", "type": "EQUITY"},
    {"epic": "1810", "name": "Xiaomi Corporation", "sector": "Smartphones & Smart Devices", "type": "EQUITY"},
    {"epic": "1211", "name": "BYD Company Ltd", "sector": "Electric Vehicles & Batteries", "type": "EQUITY"},
    {"epic": "9618", "name": "JD.com Inc", "sector": "Retail & Logistics", "type": "EQUITY"},
    {"epic": "9999", "name": "NetEase Inc", "sector": "Online Gaming", "type": "EQUITY"},
    {"epic": "9888", "name": "Baidu Inc", "sector": "Search & Autonomous AI", "type": "EQUITY"},
    {"epic": "PDD", "name": "PDD Holdings (Temu)", "sector": "Global Discount E-Commerce", "type": "EQUITY"},
    {"epic": "1024", "name": "Kuaishou Technology", "sector": "Short Video Platform", "type": "EQUITY"},
    {"epic": "2015", "name": "Li Auto Inc", "sector": "Electric SUVs", "type": "EQUITY"},
    {"epic": "9866", "name": "NIO Inc", "sector": "Premium Electric Vehicles", "type": "EQUITY"},
    {"epic": "9868", "name": "XPeng Inc", "sector": "Smart Electric Cars", "type": "EQUITY"},
    {"epic": "0175", "name": "Geely Automobile", "sector": "Auto Manufacturing", "type": "EQUITY"},
    {"epic": "0981", "name": "SMIC Semiconductor", "sector": "Chip Foundry", "type": "EQUITY"},
    {"epic": "0992", "name": "Lenovo Group", "sector": "PC & Server Hardware", "type": "EQUITY"},
    {"epic": "1299", "name": "AIA Group Ltd", "sector": "Pan-Asian Life Insurance", "type": "EQUITY"},
    {"epic": "0005", "name": "HSBC Holdings (HK)", "sector": "Commercial Banking", "type": "EQUITY"},
    {"epic": "2318", "name": "Ping An Insurance", "sector": "Integrated Financial Services", "type": "EQUITY"},
    {"epic": "0939", "name": "China Construction Bank", "sector": "Commercial Banking", "type": "EQUITY"},
    {"epic": "1398", "name": "ICBC China", "sector": "World's Largest Bank", "type": "EQUITY"},
    {"epic": "3988", "name": "Bank of China", "sector": "State-Owned Banking", "type": "EQUITY"},
    {"epic": "0388", "name": "HKEX", "sector": "Stock Exchange Operator", "type": "EQUITY"},
    {"epic": "0016", "name": "Sun Hung Kai Properties", "sector": "Hong Kong Real Estate", "type": "EQUITY"},
    {"epic": "0001", "name": "CK Hutchison Holdings", "sector": "Ports, Retail & Infrastructure", "type": "EQUITY"},
    {"epic": "0002", "name": "CLP Holdings", "sector": "Electric Power Utility", "type": "EQUITY"},
    {"epic": "0003", "name": "Hong Kong & China Gas", "sector": "Town Gas Utility", "type": "EQUITY"},
    {"epic": "0027", "name": "Galaxy Entertainment", "sector": "Gaming & Hospitality", "type": "EQUITY"},
    {"epic": "0883", "name": "CNOOC Limited", "sector": "Offshore Oil Exploration", "type": "EQUITY"},
    {"epic": "0857", "name": "PetroChina Co Ltd", "sector": "National Oil & Petrochemicals", "type": "EQUITY"},
    {"epic": "0386", "name": "Sinopec China", "sector": "Refining & Petroleum", "type": "EQUITY"},
    {"epic": "0941", "name": "China Mobile Ltd", "sector": "5G Mobile Network", "type": "EQUITY"},
    {"epic": "0762", "name": "China Unicom", "sector": "Broadband & Mobile", "type": "EQUITY"},
    {"epic": "2388", "name": "BOC Hong Kong", "sector": "Commercial Banking", "type": "EQUITY"},
    {"epic": "2319", "name": "China Mengniu Dairy", "sector": "Dairy Consumer Products", "type": "EQUITY"},
    {"epic": "1928", "name": "Sands China Ltd", "sector": "Resorts & Gaming", "type": "EQUITY"},
    {"epic": "BHP", "name": "BHP Group Ltd", "sector": "Global Natural Resources", "type": "EQUITY"},
    {"epic": "CBA", "name": "Commonwealth Bank of Australia", "sector": "Leading Australian Bank", "type": "EQUITY"},
    {"epic": "CSL", "name": "CSL Limited", "sector": "Biotherapies & Blood Plasma", "type": "EQUITY"},
    {"epic": "NAB", "name": "National Australia Bank", "sector": "Commercial Banking", "type": "EQUITY"},
    {"epic": "WBC", "name": "Westpac Banking Corp", "sector": "Retail & Business Banking", "type": "EQUITY"},
    {"epic": "ANZ", "name": "ANZ Group Holdings", "sector": "Institutional & Retail Banking", "type": "EQUITY"},
    {"epic": "WES", "name": "Wesfarmers Ltd", "sector": "Retail Conglomerate (Bunnings)", "type": "EQUITY"},
    {"epic": "MQG", "name": "Macquarie Group", "sector": "Global Infrastructure & Asset Mgmt", "type": "EQUITY"},
    {"epic": "WOW", "name": "Woolworths Group", "sector": "Food Retail & Supermarkets", "type": "EQUITY"},
    {"epic": "RIO_AU", "name": "Rio Tinto Ltd (AU)", "sector": "Iron Ore & Minerals", "type": "EQUITY"},
    {"epic": "FMG", "name": "Fortescue Metals Group", "sector": "Green Energy & Iron Ore", "type": "EQUITY"},
    {"epic": "TLS", "name": "Telstra Group Ltd", "sector": "Telecoms Leader", "type": "EQUITY"},
    {"epic": "WDS", "name": "Woodside Energy Group", "sector": "LNG & Oil Production", "type": "EQUITY"},
    {"epic": "ALL", "name": "Aristocrat Leisure", "sector": "Gaming Tech & Content", "type": "EQUITY"},
    {"epic": "GMG", "name": "Goodman Group", "sector": "Industrial Property & Logistics", "type": "EQUITY"},
    {"epic": "REA", "name": "REA Group Ltd", "sector": "Digital Property Advertising", "type": "EQUITY"},
    {"epic": "SHL", "name": "Sonic Healthcare", "sector": "Pathology & Radiology", "type": "EQUITY"},
    {"epic": "COL", "name": "Coles Group Ltd", "sector": "Supermarkets & Liquor", "type": "EQUITY"},
    {"epic": "QAN", "name": "Qantas Airways", "sector": "Airline Flag Carrier", "type": "EQUITY"},
    {"epic": "WTC", "name": "WiseTech Global", "sector": "Logistics Software (CargoWise)", "type": "EQUITY"},
    {"epic": "XRO", "name": "Xero Limited", "sector": "Cloud Accounting Software", "type": "EQUITY"},
    {"epic": "GOLD", "name": "Spot Gold / US Dollar", "sector": "Precious Metals", "type": "COMMODITY"},
    {"epic": "SILVER", "name": "Spot Silver / US Dollar", "sector": "Precious Metals", "type": "COMMODITY"},
    {"epic": "OIL_CRUDE", "name": "US WTI Crude Oil", "sector": "Commodity", "type": "COMMODITY"},
]

# ------------------------------------------------------------------------------
# 4. FAST RAM INDEXATION & LOOKUP CACHE (< 0.0001 ms)
# ------------------------------------------------------------------------------
TOP_100_US_EPICS: List[str] = [x["epic"] for x in TOP_100_US_DATA]
TOP_100_EU_EPICS: List[str] = [x["epic"] for x in TOP_100_EU_DATA]
TOP_100_ASIA_EPICS: List[str] = [x["epic"] for x in TOP_100_ASIA_DATA]

TOP_100_US_SET: Set[str] = set(TOP_100_US_EPICS)
TOP_100_EU_SET: Set[str] = set(TOP_100_EU_EPICS)
TOP_100_ASIA_SET: Set[str] = set(TOP_100_ASIA_EPICS)

ALL_TRI_REGIONAL_EPICS_SET: Set[str] = TOP_100_US_SET | TOP_100_EU_SET | TOP_100_ASIA_SET

# Maps for fast O(1) metadata lookup
EPIC_METADATA_RAM: Dict[str, Dict[str, str]] = {}
for item in TOP_100_US_DATA:
    EPIC_METADATA_RAM[item["epic"]] = {**item, "region": "US", "session": "NEW_YORK"}
for item in TOP_100_EU_DATA:
    if item["epic"] not in EPIC_METADATA_RAM:
        EPIC_METADATA_RAM[item["epic"]] = {**item, "region": "EU", "session": "LONDON"}
for item in TOP_100_ASIA_DATA:
    if item["epic"] not in EPIC_METADATA_RAM:
        EPIC_METADATA_RAM[item["epic"]] = {**item, "region": "ASIA", "session": "TOKYO_ASIA"}

COMMODITY_EPICS_SET: Set[str] = {"GOLD", "SILVER", "OIL_CRUDE", "OIL_BRENT", "NATURALGAS"}
INDEX_EPICS_SET: Set[str] = {
    "US100", "US500", "US30", "US2000",
    "DE40", "UK100", "FR40", "EU50", "SWI20", "IT40", "ES35", "NL25",
    "JP225", "J225", "HK50", "CN50", "AUS200", "AU200", "SG30", "SG25", "TW30"
}
EQUITY_EPICS_SET: Set[str] = ALL_TRI_REGIONAL_EPICS_SET - (COMMODITY_EPICS_SET | INDEX_EPICS_SET)


# ------------------------------------------------------------------------------
# 5. INSTITUTIONAL INTERBANK SESSION TIMING & ASSET ROUTING
# ------------------------------------------------------------------------------
class TriRegionalSessionRouter:
    """
    🏛️ Tri-Regional Session Timing & Dynamic Asset Routing Engine:
    Honors the exact global market trading hours (Phnom Penh ICT = UTC + 7):

    1. Tokyo / Asian Session (00:00 - 07:00 UTC = 07:00 - 14:00 ICT, Prime: 07:00 - 13:30 ICT):
       - Focus: Top 100 ASIA (JP225, HK50, CN50, AUS200, Asian equities) + GOLD + Commodities.
       - Gating: US & European equities strictly closed to avoid illiquid pre-market chop.

    2. London Open Kill Zone (07:00 - 13:30 UTC = 14:00 - 20:30 ICT, Prime: 14:00 - 18:30 ICT):
       - Focus: Top 100 EU (DE40, UK100, FR40, EU50, European equities) + GOLD + Commodities.
       - Gating: US Cash Equities locked until Wall Street Cash Open (20:30 ICT / 13:30 UTC).

    3. Wall Street New York Open Kill Zone (13:30 - 20:30 UTC = 20:30 - 03:30 ICT, Prime: 20:30 - 01:30 ICT):
       - Focus: Top 100 US (US100, US500, US30, Mega-Cap Tech, US equities) + GOLD + OIL.

    4. Overnight Rollover Swap Shield & Flat Cash (20:30 - 23:59 UTC = 03:30 - 07:00 ICT):
       - Harvest intraday gains to Flat Cash before 21:00 UTC rollover. 0 new TradFi entries.

    5. Weekend Capital Preservation Mode (Fri 20:45 - Sun 22:00 UTC):
       - TradFi markets closed, zero exposure standby.
    """

    @classmethod
    def get_current_session_code(cls, now_utc: Optional[datetime.datetime] = None) -> str:
        if now_utc is None:
            now_utc = datetime.datetime.now(datetime.timezone.utc)
        weekday = now_utc.weekday()  # Monday = 0, Sunday = 6
        utc_min = now_utc.hour * 60 + now_utc.minute

        # Weekend closure: Friday 20:45 UTC to Sunday 22:00 UTC
        if (weekday == 5) or (weekday == 4 and utc_min >= 1245) or (weekday == 6 and utc_min < 1320):
            return "WEEKEND_STANDBY"

        # Overnight Flat Cash window: 20:30 - 23:59 UTC
        if utc_min >= 1230:
            return "OVERNIGHT_FLAT_CASH"

        # Asian Session: 00:00 - 07:00 UTC (07:00 - 14:00 ICT)
        if 0 <= utc_min < 420:
            return "ASIAN_SESSION"

        # London Session: 07:00 - 13:30 UTC (14:00 - 20:30 ICT)
        if 420 <= utc_min < 810:
            return "LONDON_KILL_ZONE"

        # New York Session: 13:30 - 20:30 UTC (20:30 - 03:30 ICT)
        if 810 <= utc_min < 1230:
            return "NEW_YORK_KILL_ZONE"

        return "DEFAULT_SESSION"

    @classmethod
    def get_active_session_assets(cls, now_utc: Optional[datetime.datetime] = None) -> List[str]:
        """
        Returns dynamic asset list ordered by highest institutional edge,
        incorporating Top 100 US, Top 100 EU, Top 100 ASIA by active trading session.
        """
        sess = cls.get_current_session_code(now_utc)

        if sess == "WEEKEND_STANDBY" or sess == "OVERNIGHT_FLAT_CASH":
            return []

        if sess == "ASIAN_SESSION":
            # Primary: Commodities + Asia Core Indices + Asia Top 100 Leaders
            core = ["GOLD", "SILVER", "OIL_CRUDE", "JP225", "HK50", "CN50", "AUS200"]
            rest = [e for e in TOP_100_ASIA_EPICS if e not in core]
            return core + rest

        if sess == "LONDON_KILL_ZONE":
            # Primary: Commodities + DAX & European Indices + Europe Top 100 Leaders
            core = ["GOLD", "GERMANY40", "DE40", "OIL_CRUDE", "SILVER", "UK100", "FR40", "EU50"]
            rest = [e for e in TOP_100_EU_EPICS if e not in core]
            return core + rest

        if sess == "NEW_YORK_KILL_ZONE":
            # Primary: Core US Mega-Caps + US Indices + US Top 100 Leaders
            core = [
                "US100", "US500", "NVDA", "TSLA", "META", "GOOGL", "AAPL", "MSFT", "AMZN",
                "GOLD", "OIL_CRUDE", "US30", "GERMANY40"
            ]
            rest = [e for e in TOP_100_US_EPICS if e not in core]
            return core + rest

        # Default fallback
        return ["GOLD", "US500", "US100", "NVDA", "TSLA", "OIL_CRUDE"]

    @classmethod
    def is_asset_session_valid(cls, epic: str, now_utc: Optional[datetime.datetime] = None) -> Tuple[bool, str]:
        """
        Validates whether an epic is legally tradable during the current session window.
        """
        epic_u = str(epic or "").upper().strip()
        sess = cls.get_current_session_code(now_utc)

        if sess in ["WEEKEND_STANDBY", "OVERNIGHT_FLAT_CASH"]:
            return False, f"TRADFI_SESSION_CLOSED: TradFi markets in {sess} window."

        # Commodities are global 24/5 assets
        if epic_u in COMMODITIES_MAP:
            return True, "COMMODITY_GLOBAL_SESSION_CLEARANCE"

        # US Equities & Indices
        if epic_u in TOP_100_US_SET or any(s in epic_u for s in ["US100", "US500", "US30", "US2000"]):
            if sess != "NEW_YORK_KILL_ZONE":
                return False, f"SESSION_GATED: US instrument {epic_u} active only during New York Session (20:30-03:30 ICT)."
            return True, "NEW_YORK_SESSION_CLEARANCE"

        # European Equities & Indices
        if epic_u in TOP_100_EU_SET or any(e in epic_u for e in ["DE40", "GERMANY40", "UK100", "FR40", "EU50", "SWI20", "IT40"]):
            if sess not in ["LONDON_KILL_ZONE", "NEW_YORK_KILL_ZONE"]:
                return False, f"SESSION_GATED: European instrument {epic_u} active only during London/Europe Session (14:00-20:30 ICT)."
            return True, "EUROPEAN_SESSION_CLEARANCE"

        # Asian Equities & Indices
        if epic_u in TOP_100_ASIA_SET or any(a in epic_u for a in ["JP225", "J225", "HK50", "CN50", "AUS200", "AU200", "SG30", "SG25", "TW30"]):
            if sess != "ASIAN_SESSION":
                return False, f"SESSION_GATED: Asian instrument {epic_u} active only during Asian Session (07:00-14:00 ICT)."
            return True, "ASIAN_SESSION_CLEARANCE"

        return True, "DEFAULT_SESSION_CLEARANCE"


COMMODITIES_MAP: Set[str] = {"GOLD", "SILVER", "OIL", "OIL_CRUDE", "OIL_BRENT", "NATURALGAS", "XAUUSD", "XAGUSD"}


def get_epic_region(epic: str) -> str:
    """Returns 'US', 'EU', 'ASIA', or 'COMMODITY' in < 0.0001ms."""
    u = str(epic or "").upper().strip()
    if u in COMMODITY_EPICS_SET or u in COMMODITIES_MAP:
        return "COMMODITY"
    meta = EPIC_METADATA_RAM.get(u)
    if meta:
        return meta.get("region", "US")
    if u in TOP_100_ASIA_SET:
        return "ASIA"
    if u in TOP_100_EU_SET:
        return "EU"
    return "US"


def is_equity_asset(epic: str) -> bool:
    """Returns True if the asset is a company stock/equity (5:1 leverage / 20% margin)."""
    u = str(epic or "").upper().strip()
    return u in EQUITY_EPICS_SET


def is_index_asset(epic: str) -> bool:
    """Returns True if the asset is an index (20:1 leverage / 5% margin)."""
    u = str(epic or "").upper().strip()
    return u in INDEX_EPICS_SET


def is_commodity_asset(epic: str) -> bool:
    """Returns True if the asset is a commodity (20:1 leverage / 5% margin)."""
    u = str(epic or "").upper().strip()
    return u in COMMODITY_EPICS_SET or u in COMMODITIES_MAP


def get_tri_regional_summary() -> Dict[str, Any]:
    """Returns telemetry statistics of the Tri-Regional Universe."""
    return {
        "total_us_assets": len(TOP_100_US_DATA),
        "total_eu_assets": len(TOP_100_EU_DATA),
        "total_asia_assets": len(TOP_100_ASIA_DATA),
        "total_universe_assets": len(ALL_TRI_REGIONAL_EPICS_SET),
        "total_indices": len(INDEX_EPICS_SET),
        "total_equities": len(EQUITY_EPICS_SET),
        "total_commodities": len(COMMODITY_EPICS_SET),
        "active_session": TriRegionalSessionRouter.get_current_session_code(),
        "active_session_assets_count": len(TriRegionalSessionRouter.get_active_session_assets())
    }
