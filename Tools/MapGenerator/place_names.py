"""Random landmark names for gen_random.py (Random New World).

Every kind of landmark has a few name patterns that are filled from word lists, so each seed gets its own names instead
of the same fixed list. PlaceNames(seed) has its own random stream: the names never change the land of a seed.
Captions are plain ASCII without commas or '=' (map signs of the WBSave).
"""
import random

SURNAMES = [
    'Whitcomb', 'Harcourt', 'Ellery', 'Ashcombe', 'Tolland', 'Pembroke', 'Winthrop', 'Hartley', 'Whitmore', 'Ashby', 'Mercer',
    'Crawford', 'Halloway', 'Frobisher', 'Montgomery', 'Chester', 'Hatton', 'Bradford', 'Endicott', 'Carver', 'Standish',
    'Prescott', 'Hale', 'Langley', 'Fairfax', 'Calvert', 'Dudley', 'Sutton', 'Radcliffe', 'Thornton', 'Belden', 'Morrow',
    'Pickering', 'Hutchinson', 'Bowditch', 'Danforth', 'Kimball', 'Talcott', 'Wadsworth', 'Ingram', 'Lockwood', 'Percival',
    'Ramsay', 'Stratton', 'Vaughan', 'Whitfield', 'Aldridge', 'Barlow', 'Dunmore', 'Fenwick', 'Gilbert', 'Hawley', 'Keene',
    'Lyndon', 'Norwood', 'Osgood', 'Pell', 'Quincy', 'Rowley', 'Sewall', 'Tilden', 'Upham', 'Wendell', 'Yardley', 'Ainsworth',
    'Blackwood', 'Corbett', 'Davenport', 'Eastwick', 'Fleming', 'Gorham', 'Holbrook', 'Ives', 'Jessup', 'Kendall', 'Latham',
    'Maddox', 'Nesbitt', 'Oakes', 'Partridge', 'Royce', 'Sherwood', 'Townsend', 'Vane', 'Waverly', 'Abbott', 'Burgess',
    'Cartwright', 'Denholm', 'Everett', 'Foxworth', 'Granger', 'Hadley', 'Kirkland', 'Lowell', 'Merriweather', 'Northcote',
]
NATURE = [
    'Raven', 'Elk', 'Black', 'Kettle', 'Bear', 'Otter', 'Beaver', 'Pine', 'Cedar', 'Willow', 'Stone', 'Clear', 'Loon', 'Swan',
    'Crane', 'Heron', 'Wolf', 'Fox', 'Moose', 'Eagle', 'Hawk', 'Falcon', 'Silver', 'Copper', 'Iron', 'Granite', 'Thunder',
    'Cold', 'Deer', 'Turtle', 'Salmon', 'Trout', 'Sturgeon', 'Maple', 'Birch', 'Hemlock', 'Spruce', 'Laurel', 'Blue', 'Red',
    'White', 'Green', 'Long', 'Crooked', 'Grand', 'Little', 'Sandy', 'Rocky', 'Misty', 'Shadow', 'Lost', 'Hidden', 'Buffalo',
    'Panther', 'Lynx', 'Osprey', 'Cloud', 'Storm', 'Sunset', 'Echo', 'Whisper', 'Antler', 'Arrow', 'Flint', 'Slate', 'Amber',
    'Bramble', 'Thistle', 'Juniper', 'Aspen', 'Tamarack', 'Walnut', 'Hickory', 'Chestnut', 'Mulberry', 'Wildcat', 'Badger',
]
NATIVE = [
    'Mohegan', 'Kennebec', 'Penobscot', 'Oswego', 'Seneca', 'Tioga', 'Wabash', 'Muskegon', 'Chippewa', 'Kaskaskia', 'Pequot',
    'Shawnee', 'Ottawa', 'Ontonagon', 'Saginaw', 'Minnetonka', 'Nashoba', 'Tuscarora', 'Catawba', 'Yadkin', 'Wyandot',
    'Kiowa', 'Pawnee', 'Natchez', 'Yazoo', 'Tombigbee', 'Ocmulgee', 'Oconee', 'Chattooga', 'Mattapony', 'Rappahannock',
    'Assiniboine', 'Athabasca', 'Nipigon', 'Temagami', 'Matagami', 'Abitibi', 'Kanawha', 'Muskingum', 'Scioto', 'Wapsipinicon',
    'Allagash', 'Androscoggin', 'Housatonic', 'Merrimack', 'Pemigewasset', 'Winnipesaukee', 'Sebago', 'Moosehead', 'Waccamaw',
    'Santee', 'Edisto', 'Altamaha', 'Coosa', 'Etowah', 'Hiwassee', 'Kankakee', 'Menominee', 'Oconto', 'Wausau', 'Kalamazoo',
]
SAINTS_EN = ['Brendan', 'Kitts', 'Thomas', 'Helena', 'Martin', 'Barnabas', 'Lucia', 'Vincent', 'Patrick', 'Columba', 'Ninian',
             'Aidan', 'David', 'Andrew', 'George', 'Jude', 'Michael', 'Simon', 'Margaret', 'Agnes', 'Christopher', 'Edmund']
SAN = ['San Lorenzo', 'Santa Rosa', 'San Miguel', 'Santa Clara', 'San Isidro', 'Santa Lucia', 'San Juan', 'Santa Fe', 'San Pedro',
       'Santa Ana', 'San Gabriel', 'Santa Barbara', 'San Mateo', 'Santa Ines', 'San Bartolome', 'Santa Catalina', 'San Cristobal',
       'Santa Marta', 'San Felipe', 'Santa Cruz', 'San Antonio', 'Santa Teresa', 'San Sebastian', 'Santa Isabel', 'San Ramon']
ADJ_ES = ['Alto', 'Blanco', 'Negro', 'Verde', 'Dorado', 'Grande', 'Azul', 'Rojo', 'Pardo', 'Seco', 'Claro', 'Hermoso', 'Bravo',
          'Frio', 'Escondido', 'Viejo', 'Largo', 'Hondo', 'Chico', 'Bello', 'Oscuro', 'Salado', 'Sereno', 'Tranquilo', 'Encantado']
ADJ_ES_F = ['Alta', 'Blanca', 'Negra', 'Verde', 'Dorada', 'Grande', 'Azul', 'Roja', 'Parda', 'Seca', 'Clara', 'Hermosa', 'Brava',
            'Fria', 'Escondida', 'Vieja', 'Larga', 'Honda', 'Chica', 'Bella', 'Oscura', 'Salada', 'Serena', 'Encantada']
ADJ_PT = ['Verde', 'Branca', 'Dourada', 'Negra', 'Azul', 'Grande', 'Alta', 'Clara', 'Bonita', 'Escura', 'Velha', 'Fria', 'Brava']
NOUN_ES = ['Plata', 'Oro', 'Cobre', 'Fuego', 'Viento', 'Sol', 'Luna', 'Niebla', 'Piedra', 'Nieve', 'Cielo', 'Agua', 'Sal',
           'las Nubes', 'los Condores', 'las Aguilas', 'los Lobos', 'las Flores', 'los Reyes', 'la Cruz', 'la Paz', 'la Luz']
NOUN_PT = ['do Mar', 'do Sol', 'da Lua', 'da Prata', 'do Ouro', 'das Neves', 'dos Ventos', 'da Esperanca', 'das Aguas', 'do Norte']
ROYALS = ['Rupert', 'Albert', 'Edward', 'Charles', 'William', 'Frederick', 'George', 'Henry', 'Leopold', 'Augustus', 'Louis']
VIRTUES = ['Mercy', 'Hope', 'Desire', 'Refuge', 'Comfort', 'Plenty', 'Haven', 'Deliverance', 'Patience', 'Providence', 'Charity',
           'Faith', 'Constance', 'Prudence', 'Liberty', 'Fortune', 'Resolution', 'Endeavour', 'Good Hope', 'Welcome', 'Repose']
COLOURS = ['Red Rock', 'Painted', 'Vermilion', 'Crimson', 'Ochre', 'Golden', 'Copper', 'Rose', 'Amber', 'Rust', 'Sunset', 'Cinnabar']
WINDS = ['Windward', 'Leeward', 'Sunrise', 'Coral', 'Pearl', 'Turtle', 'Spice', 'Fortune', 'Summer', 'Emerald', 'Sapphire', 'Gull',
         'Trade Wind', 'Halcyon', 'Sargasso', 'Morning', 'Palm', 'Nutmeg', 'Hurricane', 'Lantern']
NORSE = ['Markland', 'Helluland', 'Thule', 'Nordland', 'Halogaland', 'Vestfold', 'Hordaland', 'Ultima Thule', 'Skraeling',
         'Bjarni', 'Leifs', 'Eiriks', 'Thorvald', 'Gudrid', 'Karlsefni', 'Freydis']
MAYAN = ['Huaynacocha', 'Xunantal', 'Ixkalan', 'Tzimbal', 'Cobanex', 'Yaxhal', 'Chacpetun', 'Kinichna', 'Uxbenal', 'Pacalmun',
         'Huaylla', 'Tikalpa', 'Ochmaya', 'Zacpeten', 'Itzamal', 'Balamku', 'Nohoch', 'Tzunkal', 'Chumbeh', 'Quiriguax']
ALTIPLANO = ['Sorata', 'Achacachi', 'Carangas', 'Lipez', 'Pacajes', 'Omasuyos', 'Chucuito', 'Yungas', 'Huarina', 'Ancoraimes',
             'Tiquina', 'Copacabana', 'Caquiaviri', 'Ayopaya']
VALLEYS = ['Paradise', 'Eden', 'Sleepy', 'Golden', 'Happy', 'Lost', 'Hidden', 'Shangri', 'Elysian', 'Arcadia', 'Avalon', 'Serenity']
ANIMALS_ES = ['Toro', 'Venado', 'Agua', 'Coyote', 'Halcon', 'Lobo', 'Puma', 'Caballo', 'Cuervo', 'Zorro']
REGIONS = {
    'boreal': ['New Caledonia', 'Keewatin', 'Rupertsland', 'Assiniboia', 'New North Wales', 'Athabasca', 'Ungava', 'Nipissing',
               'New South Wales', 'Labrador', 'Kitikmeot', 'Mistassini'],
    'temperate': ['New Albion', 'Acadia', 'New Hanover', 'Carolana', 'New Sweden', 'New Holland', 'Laconia', 'Mariana',
                  'New Somerset', 'Transylvania', 'Westsylvania', 'New Connaught', 'Vandalia', 'Norumbega', 'New Cornwall',
                  'New Essex', 'Lygonia', 'New Scotland', 'Mount Desert', 'New Ireland', 'Charlotina', 'Pittsylvania'],
    'subtropical': ['Nueva Galicia', 'Vera Paz', 'Nueva Vizcaya', 'Nueva Extremadura', 'Nuevo Santander', 'Florida Oriental',
                    'Tejas', 'Nueva Navarra', 'Nuevo Leon', 'Apalache', 'Guale', 'Timucua', 'Nueva Asturias'],
    'south': ['Terra de Santa Cruz', 'Nueva Andalucia', 'Tierra Firme', 'Nueva Granada', 'Castilla de Oro', 'Nueva Toledo',
              'Vera Cruz', 'Terra Nova do Sul', 'Nueva Cordoba', 'Paraguaia', 'Nueva Castilla', 'Terra de Vera Cruz',
              'Nueva Valencia', 'Provincia Aurea'],
}

# kind -> name patterns; {S} surname, {N} nature word, {I} native name, {E} English saint, {X} San/Santa, {A}/{F} Spanish
# adjective (m/f), {P} Portuguese adjective, {O} Spanish noun, {Q} Portuguese noun, {R} royal name, {V} virtue, {C} colour,
# {W} wind/isle word, {K} Norse name, {M} Mayan name, {L} altiplano place, {Y} valley word, {Z} Spanish animal
PATTERNS = {
    'peak_n': ['Mount {S}', 'Mount {S}', '{N} Peak', '{N} Dome', 'Mount {N}', '{S} Peak', 'Old {N} Knob'],
    'range_n': ['{S} Range', '{N} Range', '{N} Ridge', '{N} Mountains', '{S} Mountains', '{I} Mountains', '{N} Hills'],
    'peak_s': ['Cerro {A}', 'Nevado {X}', 'Pico {A}', 'Cerro {X}', 'Nevado {A}', 'Pico {Q}'],
    'range_s': ['Sierra {F}', 'Cordillera {F}', 'Serra {P}', 'Sierra de {O}', 'Cordillera de {X}', 'Serra {Q}'],
    'river_n': ['{N} River', '{I} River', '{S} River', 'Saint {E} River', '{I} River'],
    'river_s': ['Rio {A}', 'Rio {X}', 'Rio de {O}', 'Rio {Q}'],
    'lake_n': ['Lake {S}', '{N} Lake', 'Lake {I}', 'Lake {S}', '{I} Lake'],
    'lake_s': ['Laguna {F}', 'Lago {A}', 'Laguna de {X}', 'Lagoa {P}'],
    'volcano_isle': ['Saint {E} Island', '{X} Island', 'Isla {X}'],
    'crater': ['{S} Crater', '{N} Crater', '{N} Bowl'],
    'canyon': ['{C} Canyon', '{N} Canyon', '{S} Canyon'],
    'valley': ['{Y} Valley', '{N} Valley', '{S} Valley'],
    'gorge': ['{S} Gorge', '{N} Gorge', '{I} Gorge'],
    'river_isle': ['{N} Island', '{S} Island', '{I} Island'],
    'estuary': ['{S} Bay', '{I} Bay', '{N} Bay'],
    'banks': ['{S} Banks', '{N} Banks', '{N} Shoals', '{S} Shoals'],
    'finger_lakes': ['{I} Lakes', '{N} Lakes', '{S} Lakes'],
    'salt_basin': ['Great Salt Basin', '{N} Salt Flats', '{S} Salt Basin', '{C} Salt Flats', 'Bitter Basin'],
    'altiplano': ['Altiplano de {L}', 'Puna de {L}', 'Altiplano {A}'],
    'mesas': ['{C} Mesas', 'Painted Mesas', 'Enchanted Mesas', '{N} Mesas', '{S} Buttes'],
    'oasis': ['{N} Springs', 'Agua {F}', 'Ojo del {Z}', '{S} Springs', 'Bitter Springs', 'Ojo de {X}'],
    'strait': ['{S} Strait', '{K} Strait', '{R} Strait'],
    'arctic_isle': ['Prince {R} Island', '{S} Island', '{K} Island', 'King {R} Island'],
    'isles': ['{W} Isles', '{W} Islands', 'Islas de {X}', '{W} Keys'],
    'harbour': ['{V} Bay', '{V} Sound', 'Port {V}', '{V} Harbour'],
    'fjords': ['{K} Coast', '{K} Fjords', '{N} Fjords'],
    'volcano': ['Volcan {X}', 'Volcan {A}', 'Cerro Humeante', 'Volcan de {O}', 'Cerro {X}'],
    'lost_city': ['Ciudad Perdida', 'Ciudad Blanca', 'Ciudad de los Dioses', 'Ciudad Escondida', 'Ruinas de {M}'],
    'ruins': ['Ruinas de {M}', 'Templo de {M}', 'Ruinas de {M}'],
    'caldera': ['Cerros Redondos', '{S} Caldera', 'Crater Hills', 'Cerros de {X}'],
}
WORDS = {'S': SURNAMES, 'N': NATURE, 'I': NATIVE, 'E': SAINTS_EN, 'X': SAN, 'A': ADJ_ES, 'F': ADJ_ES_F, 'P': ADJ_PT,
         'O': NOUN_ES, 'Q': NOUN_PT, 'R': ROYALS, 'V': VIRTUES, 'C': COLOURS, 'W': WINDS, 'K': NORSE, 'M': MAYAN,
         'L': ALTIPLANO, 'Y': VALLEYS, 'Z': ANIMALS_ES}


class PlaceNames(object):
    def __init__(self, seed):
        self.rng = random.Random(seed * 131 + 17)
        self.used = set()
        self.words_used = set()
        self.regions = {}
        for zone in sorted(REGIONS):
            names = list(REGIONS[zone])
            self.rng.shuffle(names)
            self.regions[zone] = names

    def fill(self, pattern):
        out = ''
        i = 0
        while i < len(pattern):
            c = pattern[i]
            if c == '{':
                key = pattern[i + 1]
                words = WORDS[key]
                fresh = [w for w in words if w not in self.words_used]
                w = self.rng.choice(fresh or words)
                self.words_used.add(w)       # a word appears in only one name of the map while there are unused ones
                out += w
                i += 3
            else:
                out += c
                i += 1
        return out

    def name(self, kind):
        """A new name of this kind, not used before on this map."""
        caption = None
        for _ in range(40):
            caption = self.fill(self.rng.choice(PATTERNS[kind]))
            if caption not in self.used:
                break
        self.used.add(caption)
        return caption

    def names(self, kind, n):
        return [self.name(kind) for _ in range(n)]

    def region(self, zone):
        """The next regional name of a climate zone, or None when they are used up."""
        names = self.regions[zone]
        while names:
            caption = names.pop(0)
            if caption not in self.used:
                self.used.add(caption)
                return caption
        return None
