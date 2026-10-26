"""
Crop Knowledge Database & Agronomic Specifications
Contains rich agronomic intelligence, ideal conditions, cultivation timelines,
and economic data for all 22 supported crops.
"""

CROPS_DATA = {
    "rice": {
        "name": "Rice",
        "scientific_name": "Oryza sativa",
        "category": "Cereal / Food Grain",
        "icon": "🌾",
        "season": "Kharif (Monsoon)",
        "duration": "100 - 150 days",
        "soil_type": "Clayey, Clay-Loam, Alluvial with high water retention",
        "water_requirement": "High (1200 - 2000 mm)",
        "optimal_ranges": {"N": "60-100", "P": "35-60", "K": "35-45", "temp": "20-27°C", "humidity": "80-85%", "ph": "5.5-7.2", "rainfall": "180-300 mm"},
        "economic_value": "High staple demand; High domestic and global export market.",
        "best_practices": [
            "Maintain 2-5 cm standing water during vegetative stage.",
            "Use Azospirillum and Phosphobacteria bio-fertilizers for better yield.",
            "Transplant 20-25 day old seedlings in puddle fields."
        ],
        "fertilizer_guide": "Basal dose of NPK + 2 split top-dressings of Urea during tillering and panicle initiation."
    },
    "maize": {
        "name": "Maize (Corn)",
        "scientific_name": "Zea mays",
        "category": "Cereal / Coarse Grain",
        "icon": "🌽",
        "season": "Kharif / Rabi / Spring",
        "duration": "90 - 120 days",
        "soil_type": "Well-drained deep loamy soil rich in organic matter",
        "water_requirement": "Moderate (500 - 800 mm)",
        "optimal_ranges": {"N": "60-100", "P": "35-60", "K": "15-25", "temp": "18-27°C", "humidity": "55-75%", "ph": "5.5-7.5", "rainfall": "60-110 mm"},
        "economic_value": "High demand in livestock feed, starch industry, bio-ethanol, and food products.",
        "best_practices": [
            "Ensure proper drainage; maize is sensitive to waterlogging.",
            "Plant at 60cm row spacing and 20cm plant spacing.",
            "Apply zinc sulfate at 25 kg/ha if zinc deficiency is observed."
        ],
        "fertilizer_guide": "High nitrogen demanding crop. Apply N in 3 splits (sowing, knee-high stage, and tasseling)."
    },
    "chickpea": {
        "name": "Chickpea (Gram)",
        "scientific_name": "Cicer arietinum",
        "category": "Pulse / Legume",
        "icon": "🌱",
        "season": "Rabi (Winter)",
        "duration": "90 - 120 days",
        "soil_type": "Sandy-loam to clay-loam, well drained",
        "water_requirement": "Low (250 - 400 mm)",
        "optimal_ranges": {"N": "20-60", "P": "55-80", "K": "75-85", "temp": "17-20°C", "humidity": "14-19%", "ph": "6.0-8.5", "rainfall": "65-95 mm"},
        "economic_value": "Premier pulse crop with high protein content; major protein source in vegetarian diets.",
        "best_practices": [
            "Inoculate seeds with Rhizobium culture before sowing.",
            "Nip apical buds at 30-40 days to encourage profuse branching.",
            "Avoid excessive moisture during flowering to prevent pod drop."
        ],
        "fertilizer_guide": "Fixes atmospheric nitrogen. Low N requirement, responds well to Phosphorus and Sulfur."
    },
    "kidneybeans": {
        "name": "Kidney Beans (Rajma)",
        "scientific_name": "Phaseolus vulgaris",
        "category": "Pulse / Legume",
        "icon": "🫘",
        "season": "Rabi in plains / Kharif in hills",
        "duration": "100 - 130 days",
        "soil_type": "Deep, well-drained fertile loam with good organic matter",
        "water_requirement": "Moderate (400 - 600 mm)",
        "optimal_ranges": {"N": "15-40", "P": "55-80", "K": "15-25", "temp": "15-24°C", "humidity": "18-25%", "ph": "5.5-6.5", "rainfall": "60-150 mm"},
        "economic_value": "High commercial value, excellent profit margins in North Indian markets.",
        "best_practices": [
            "Does not fix atmospheric nitrogen effectively; requires supplemental nitrogen.",
            "Maintain ridge and furrow planting to avoid water stagnation.",
            "Irrigate at critical stages: flowering and pod development."
        ],
        "fertilizer_guide": "Apply 100 kg N, 60 kg P2O5, and 30 kg K2O per hectare for maximum pod yield."
    },
    "pigeonpeas": {
        "name": "Pigeon Peas (Arhar / Tur)",
        "scientific_name": "Cajanus cajan",
        "category": "Pulse / Legume",
        "icon": "🌿",
        "season": "Kharif",
        "duration": "150 - 200 days",
        "soil_type": "Deep loamy to clayey soil with good drainage",
        "water_requirement": "Moderate (600 - 800 mm)",
        "optimal_ranges": {"N": "10-40", "P": "55-80", "K": "15-25", "temp": "27-38°C", "humidity": "30-65%", "ph": "5.0-7.5", "rainfall": "90-200 mm"},
        "economic_value": "Staple dal across India, stable long-term market pricing.",
        "best_practices": [
            "Deep taproot system makes it exceptionally drought tolerant.",
            "Excellent for intercropping with soybean, groundnut, or cotton.",
            "Provide one protective irrigation at pod-filling stage if drought occurs."
        ],
        "fertilizer_guide": "Apply DAP at 100 kg/ha at time of sowing along with Rhizobium seed coating."
    },
    "mothbeans": {
        "name": "Moth Beans (Matki)",
        "scientific_name": "Vigna aconitifolia",
        "category": "Pulse / Arid Legume",
        "icon": "🌾",
        "season": "Kharif (Arid & Semi-arid)",
        "duration": "75 - 90 days",
        "soil_type": "Sandy to sandy-loam, light soils",
        "water_requirement": "Very Low (200 - 400 mm)",
        "optimal_ranges": {"N": "0-40", "P": "35-60", "K": "15-25", "temp": "24-32°C", "humidity": "40-65%", "ph": "3.5-9.0", "rainfall": "30-75 mm"},
        "economic_value": "Drought-hardy superfood, used in namkeens (Bikaneri Bhujia) and sprouts.",
        "best_practices": [
            "Extreme drought tolerance; survives on minimal residual moisture.",
            "Prevents soil erosion in desert and dryland environments.",
            "Requires minimal weed management once canopy covers the soil."
        ],
        "fertilizer_guide": "Low fertilizer demand. 20 kg N + 40 kg P2O5 per hectare is sufficient."
    },
    "mungbean": {
        "name": "Mung Bean (Green Gram)",
        "scientific_name": "Vigna radiata",
        "category": "Pulse / Short Duration",
        "icon": "🌱",
        "season": "Kharif / Summer / Zaid",
        "duration": "60 - 75 days",
        "soil_type": "Well-drained loamy to sandy-loam soil",
        "water_requirement": "Low (350 - 500 mm)",
        "optimal_ranges": {"N": "10-40", "P": "35-60", "K": "15-25", "temp": "27-30°C", "humidity": "80-90%", "ph": "6.2-7.2", "rainfall": "35-60 mm"},
        "economic_value": "Short crop rotation cycle allows multiple harvests per year; high market liquidity.",
        "best_practices": [
            "Ideal for catch cropping between Rabi harvest and Kharif sowing.",
            "Treat seed with Trichoderma for root-rot management.",
            "Pick mature pods in morning hours to prevent shattering."
        ],
        "fertilizer_guide": "Basal application of 20 kg N and 40 kg P2O5 per ha; spray 2% DAP at flowering."
    },
    "blackgram": {
        "name": "Black Gram (Urad)",
        "scientific_name": "Vigna mungo",
        "category": "Pulse / Legume",
        "icon": "🫘",
        "season": "Kharif / Spring",
        "duration": "70 - 90 days",
        "soil_type": "Heavier soils, loamy or clayey with good drainage",
        "water_requirement": "Moderate (400 - 600 mm)",
        "optimal_ranges": {"N": "30-60", "P": "55-80", "K": "15-25", "temp": "25-35°C", "humidity": "60-70%", "ph": "6.5-7.8", "rainfall": "60-75 mm"},
        "economic_value": "Essential for traditional culinary staples (dosa, idli, dal makhani); premium price.",
        "best_practices": [
            "Improves soil nitrogen through symbiotic fixation.",
            "Sow in rows 30 cm apart with 10 cm plant distance.",
            "Manage yellow mosaic virus by controlling whitefly vectors."
        ],
        "fertilizer_guide": "Apply 25 kg N, 50 kg P2O5, 20 kg K2O, and 20 kg Sulfur per hectare."
    },
    "lentil": {
        "name": "Lentil (Masoor)",
        "scientific_name": "Lens culinaris",
        "category": "Pulse / Winter Crop",
        "icon": "🍲",
        "season": "Rabi",
        "duration": "110 - 130 days",
        "soil_type": "Alluvial, light loams to moderate clays",
        "water_requirement": "Low (300 - 450 mm)",
        "optimal_ranges": {"N": "10-40", "P": "55-80", "K": "15-25", "temp": "18-30°C", "humidity": "60-70%", "ph": "5.5-8.0", "rainfall": "35-55 mm"},
        "economic_value": "High export potential and major dietary staple with rich iron and zinc.",
        "best_practices": [
            "Cold tolerant in early vegetative stages.",
            "Inoculate with Rhizobium leguminosarum strain before planting.",
            "Provide light irrigation at pre-flowering and pod-formation stages."
        ],
        "fertilizer_guide": "Basal dose: 20 kg N and 40 kg P2O5 per ha. Responds well to Zinc and Molybdenum."
    },
    "pomegranate": {
        "name": "Pomegranate (Anar)",
        "scientific_name": "Punica granatum",
        "category": "Fruit / Perennial Horticultural",
        "icon": "🍎",
        "season": "Year-round (Bahar treatment: Mrig/Ambe/Hasta)",
        "duration": "Perennial (Fruits in 120-150 days after flowering)",
        "soil_type": "Deep loamy or alluvial soil with pH 6.5 - 7.5",
        "water_requirement": "Moderate (Drip irrigation recommended)",
        "optimal_ranges": {"N": "15-40", "P": "10-30", "K": "35-45", "temp": "18-25°C", "humidity": "85-95%", "ph": "5.5-7.5", "rainfall": "100-115 mm"},
        "economic_value": "Very high return on investment; booming domestic and export demand (Bhagwa variety).",
        "best_practices": [
            "Adopt drip irrigation with fertigation for uniform fruit size.",
            "Prune water shoots and crisscrossing branches regularly.",
            "Regulate Bahar to target peak market price periods."
        ],
        "fertilizer_guide": "Annual per tree: 600g N, 200g P2O5, and 600g K2O applied in 3 split doses."
    },
    "banana": {
        "name": "Banana",
        "scientific_name": "Musa acuminata",
        "category": "Fruit / High Value",
        "icon": "🍌",
        "season": "Year-round Planting",
        "duration": "11 - 14 months",
        "soil_type": "Deep, rich, loamy soil with high organic matter",
        "water_requirement": "High (1500 - 2200 mm)",
        "optimal_ranges": {"N": "80-120", "P": "70-95", "K": "45-55", "temp": "25-30°C", "humidity": "75-85%", "ph": "5.5-7.0", "rainfall": "90-120 mm"},
        "economic_value": "High continuous cash flow crop with massive domestic consumption.",
        "best_practices": [
            "Use tissue-cultured Grand Naine (G9) plantlets for disease-free high yields.",
            "Ensure effective drainage; stagnant water causes Panama wilt.",
            "Provide propping support with bamboo poles during bunch development."
        ],
        "fertilizer_guide": "High potassium feeder. 200g N, 60g P, 300g K per plant divided across growth stages."
    },
    "mango": {
        "name": "Mango",
        "scientific_name": "Mangifera indica",
        "category": "Fruit / Orchard",
        "icon": "🥭",
        "season": "Perennial (Flowering in winter, harvest in summer)",
        "duration": "Perennial (4-5 months from flowering to fruit)",
        "soil_type": "Deep, well-drained alluvial or red loamy soil",
        "water_requirement": "Moderate (700 - 1200 mm)",
        "optimal_ranges": {"N": "10-40", "P": "15-35", "K": "25-35", "temp": "27-36°C", "humidity": "45-55%", "ph": "5.5-7.5", "rainfall": "85-105 mm"},
        "economic_value": "King of Fruits; premium domestic and international export market.",
        "best_practices": [
            "Withhold irrigation 2-3 months prior to flowering to promote floral induction.",
            "Use Paclobutrazol for regular bearing in alternate-bearing varieties.",
            "Spray micro-nutrients (Boron, Zinc, Copper) during fruit setting."
        ],
        "fertilizer_guide": "For bearing trees: 1 kg N, 0.5 kg P2O5, 1 kg K2O applied post-monsoon."
    },
    "grapes": {
        "name": "Grapes",
        "scientific_name": "Vitis vinifera",
        "category": "Fruit / Commercial Horticultural",
        "icon": "🍇",
        "season": "Perennial (Pruning in April & October)",
        "duration": "120 - 150 days per cycle",
        "soil_type": "Sandy loam to clay loam with good drainage, pH 6.5-8.0",
        "water_requirement": "Moderate (Drip irrigation essential)",
        "optimal_ranges": {"N": "15-40", "P": "120-145", "K": "195-205", "temp": "10-40°C", "humidity": "80-85%", "ph": "5.5-6.5", "rainfall": "65-75 mm"},
        "economic_value": "Extremely lucrative cash crop for table grapes, raisins, and wine production.",
        "best_practices": [
            "Adopt Bower (Y-trellis) training system for optimal sunlight interception.",
            "Use Gibberellic Acid (GA3) dip for berry elongation and bunch loosening.",
            "Maintain strict powdery and downy mildew spray schedule."
        ],
        "fertilizer_guide": "Very high Potassium and Phosphorus demand. Fertigation with 0:52:34 and 0:0:50."
    },
    "watermelon": {
        "name": "Watermelon",
        "scientific_name": "Citrullus lanatus",
        "category": "Fruit / Cucurbit",
        "icon": "🍉",
        "season": "Summer / Zaid",
        "duration": "80 - 100 days",
        "soil_type": "Sandy, sandy-loam with warm drainage",
        "water_requirement": "Moderate (400 - 600 mm)",
        "optimal_ranges": {"N": "80-120", "P": "10-30", "K": "45-55", "temp": "24-28°C", "humidity": "80-90%", "ph": "6.0-7.0", "rainfall": "40-60 mm"},
        "economic_value": "Fast cash return crop with high summer seasonal demand.",
        "best_practices": [
            "Use silver-black plastic mulch to conserve moisture and suppress weeds.",
            "Install drip irrigation; avoid overhead watering to prevent leaf diseases.",
            "Place beehives in orchard to ensure excellent cross-pollination."
        ],
        "fertilizer_guide": "Apply 100 kg N, 50 kg P2O5, and 50 kg K2O/ha. Boost potassium at fruit development."
    },
    "muskmelon": {
        "name": "Muskmelon (Kharbuja)",
        "scientific_name": "Cucumis melo",
        "category": "Fruit / Cucurbit",
        "icon": "🍈",
        "season": "Summer / Zaid",
        "duration": "75 - 90 days",
        "soil_type": "Sandy loam, riverbed alluvium, well-drained",
        "water_requirement": "Moderate (400 - 500 mm)",
        "optimal_ranges": {"N": "80-120", "P": "10-30", "K": "45-55", "temp": "27-30°C", "humidity": "90-95%", "ph": "6.0-7.0", "rainfall": "20-30 mm"},
        "economic_value": "High consumer demand in hot weather; great profitability in riverbeds and dry zones.",
        "best_practices": [
            "Riverbed (Diyara) cultivation is highly suited for sweet melon production.",
            "Stop watering 5-7 days before harvest to enhance sugar sweetness (Brix).",
            "Harvest at full slip stage for immediate consumption or half-slip for shipping."
        ],
        "fertilizer_guide": "80 kg N, 40 kg P2O5, and 40 kg K2O per hectare with micronutrient foliar spray."
    },
    "apple": {
        "name": "Apple",
        "scientific_name": "Malus domestica",
        "category": "Fruit / Temperate Orchard",
        "icon": "🍎",
        "season": "Temperate (Harvest July - October)",
        "duration": "Perennial (130 - 160 days from bloom to harvest)",
        "soil_type": "Deep, well-drained loamy soil rich in organic matter",
        "water_requirement": "Moderate (1000 - 1250 mm distributed rainfall)",
        "optimal_ranges": {"N": "15-40", "P": "120-145", "K": "195-205", "temp": "21-24°C", "humidity": "90-95%", "ph": "5.5-6.5", "rainfall": "100-125 mm"},
        "economic_value": "Premium fruit with exceptional cold-storage and national market value.",
        "best_practices": [
            "Requires 800 - 1100 chilling hours below 7°C for breaking dormancy.",
            "Prune during dormant winter months to establish central leader tree architecture.",
            "Apply Calcium Chloride sprays to avoid bitter pit disorders in fruit."
        ],
        "fertilizer_guide": "High K and P requirement. 700g N, 350g P2O5, 700g K2O per mature tree annually."
    },
    "orange": {
        "name": "Orange (Citrus)",
        "scientific_name": "Citrus sinensis",
        "category": "Fruit / Citrus",
        "icon": "🍊",
        "season": "Subtropical (Winter Harvest)",
        "duration": "Perennial (8-9 months from fruit set)",
        "soil_type": "Light loamy to deep alluvial soils with excellent drainage",
        "water_requirement": "Moderate (800 - 1100 mm)",
        "optimal_ranges": {"N": "15-40", "P": "10-30", "K": "5-15", "temp": "15-35°C", "humidity": "90-95%", "ph": "6.0-7.5", "rainfall": "100-120 mm"},
        "economic_value": "Massive consumer demand for fresh fruit and juice processing industries.",
        "best_practices": [
            "Avoid planting in waterlogged or heavy black clay soils to prevent Phytophthora root rot.",
            "Use disease-free budded plants on Rangpur lime or Rough lemon rootstocks.",
            "Foliar sprays of Zinc and Iron prevent citrus leaf chlorosis."
        ],
        "fertilizer_guide": "600g N, 200g P, 300g K per mature tree split across spring and monsoon."
    },
    "papaya": {
        "name": "Papaya",
        "scientific_name": "Carica papaya",
        "category": "Fruit / Tropical",
        "icon": "🍈",
        "season": "Year-round (Spring / Monsoon planting)",
        "duration": "9 - 12 months for first harvest",
        "soil_type": "Deep, well-drained sandy loam or alluvial soil",
        "water_requirement": "Moderate (Avoid stagnant moisture)",
        "optimal_ranges": {"N": "40-70", "P": "50-70", "K": "45-55", "temp": "25-35°C", "humidity": "90-95%", "ph": "6.0-7.0", "rainfall": "140-250 mm"},
        "economic_value": "Fast-yielding commercial fruit with continuous weekly fruiting and harvesting.",
        "best_practices": [
            "Plant on raised beds of 30cm height to ensure zero waterlogging.",
            "Select gynodioecious varieties like Red Lady 786 for 100% fruit-bearing plants.",
            "Spray neem oil to prevent aphid vectors transmitting Papaya Ringspot Virus."
        ],
        "fertilizer_guide": "Heavy feeder: 250g N, 250g P2O5, 500g K2O per plant per year in 6 split bi-monthly doses."
    },
    "coconut": {
        "name": "Coconut",
        "scientific_name": "Cocos nucifera",
        "category": "Plantation / Palm",
        "icon": "🥥",
        "season": "Coastal / Tropical (Year-round production)",
        "duration": "Perennial (5-6 years for first yield, productive for 60+ yrs)",
        "soil_type": "Sandy, coastal alluvium, red sandy loam, laterite",
        "water_requirement": "High (1300 - 2500 mm well distributed)",
        "optimal_ranges": {"N": "15-40", "P": "10-30", "K": "25-35", "temp": "25-30°C", "humidity": "95-100%", "ph": "5.2-8.0", "rainfall": "130-220 mm"},
        "economic_value": "Kalpavriksha (Tree of Life); continuous monthly yield of tender coconut, copra, coir, and oil.",
        "best_practices": [
            "Thrives in humid tropical coastal belts with abundant sunshine.",
            "Maintain ring basin irrigation around palms during dry periods.",
            "Apply common salt (NaCl) at 1 kg/palm/year to stimulate potash absorption."
        ],
        "fertilizer_guide": "Per adult palm: 500g N, 320g P2O5, 1200g K2O and 1 kg Magnesium Sulfate annually."
    },
    "cotton": {
        "name": "Cotton (White Gold)",
        "scientific_name": "Gossypium hirsutum",
        "category": "Fiber / Cash Crop",
        "icon": "🪴",
        "season": "Kharif",
        "duration": "150 - 180 days",
        "soil_type": "Deep black cotton soils (Vertisols) or alluvial soils",
        "water_requirement": "Moderate (500 - 750 mm)",
        "optimal_ranges": {"N": "100-140", "P": "35-60", "K": "15-25", "temp": "22-30°C", "humidity": "75-85%", "ph": "6.0-8.0", "rainfall": "60-100 mm"},
        "economic_value": "World's leading natural fiber crop; huge textile supply chain foundation.",
        "best_practices": [
            "High requirement for sunshine during squaring and boll opening stages.",
            "Use Bt-cotton hybrids with integrated pest management (IPM) for bollworms.",
            "Apply growth regulator Mepiquat Chloride to control excessive vegetative growth."
        ],
        "fertilizer_guide": "Apply 120 kg N, 60 kg P2O5, 60 kg K2O per ha with split nitrogen application."
    },
    "jute": {
        "name": "Jute (Golden Fiber)",
        "scientific_name": "Corchorus olitorius",
        "category": "Fiber / Commercial",
        "icon": "🌾",
        "season": "Kharif / Pre-Monsoon",
        "duration": "120 - 150 days",
        "soil_type": "Alluvial loamy or sandy loam soils in river deltas",
        "water_requirement": "High (1200 - 1800 mm)",
        "optimal_ranges": {"N": "60-100", "P": "35-60", "K": "35-45", "temp": "24-35°C", "humidity": "70-90%", "ph": "6.0-7.5", "rainfall": "150-200 mm"},
        "economic_value": "Biodegradable natural fiber with increasing demand in eco-friendly packaging and textiles.",
        "best_practices": [
            "Harvest at 50% flowering stage for the finest fiber tensile strength.",
            "Retting process requires clean, slow-flowing water for 12-15 days.",
            "Maintain high seedbed aeration to support rapid seedling germination."
        ],
        "fertilizer_guide": "Apply 60 kg N, 30 kg P2O5, and 30 kg K2O/ha. Top-dress nitrogen in two split doses."
    },
    "coffee": {
        "name": "Coffee",
        "scientific_name": "Coffea arabica / canephora",
        "category": "Plantation / Beverage Cash Crop",
        "icon": "☕",
        "season": "Perennial (Hill Tracts / Shade Grown)",
        "duration": "Perennial (9 months from blossom to berry ripening)",
        "soil_type": "Rich, porous, volcanic or deep lateritic loams rich in humus",
        "water_requirement": "High (1500 - 2500 mm distributed rainfall)",
        "optimal_ranges": {"N": "80-120", "P": "15-35", "K": "25-35", "temp": "22-28°C", "humidity": "50-70%", "ph": "6.0-6.8", "rainfall": "120-200 mm"},
        "economic_value": "Global commodity cash crop; high export realization for Arabica and Robusta.",
        "best_practices": [
            "Cultivate under two-tier shade trees (Silver Oak, Erythrina) to prevent leaf scorch.",
            "Blossom showers in March-April are crucial for synchronous flowering and fruit set.",
            "Prune weak and diseased branches after the winter harvest."
        ],
        "fertilizer_guide": "Balanced NPK: 120 kg N, 90 kg P2O5, 120 kg K2O per hectare applied in 4 split doses."
    }
}
