import random

import factory

from django.db.models.signals import post_save

from data.models import Canteen
from data.models.sector import Sector

from .sector import SectorM2MFactory
from .user import UserFactory

SIRET_LIST_USED_IN_TESTS = [
    "21340172201787",  # commune de montpellier
    "21380185500015",  # commune de grenoble
    "21670482500019",  # commune de strasbourg
    "21640122400011",  # commune de biarritz
    "21630113500010",  # commune de clermont-ferrand
    "21130055300016",  # commune de marseille
    "21730065600014",  # commune de chambery
    "21590350100017",  # commune de lille
    "21010034300016",  # commune de belley
    "92341284500011",  # turbine roubaix
    "40419443300078",  # peniche/turbine grenoble
    "83014132100034",  # multi coop
    "11007001800012",  # ministère de l'agriculture
]

SIREN_LIST_USED_IN_TESTS = []

SIRET_LIST_FOR_FACTORY = [
    "21070017500016",
    "26750031200017",
    "19931143200017",
    "19931231500013",
    "19931490700015",
    "19932223100010",
    "19930865100017",
    "19931232300017",
    "19931489900014",
    "19931230700028",
    "20004551600016",
    "19930893300019",
    "19931145700014",
    "19931224000021",
    "19932234800012",
    "19931225700025",
    "19931206700010",
    "19931428700012",
    "19931223200010",
    "19931229900019",
    "19931207500013",
    "19931147300011",
    "19931765200014",
    "19930891700012",
    "20004547400018",
    "19931379200012",
    "19931377600015",
    "20008049700015",
    "19930089800020",
    "19931979900011",
    "19931190300017",
    "19930100300026",
    "19931434500018",
    "19932232200017",
    "19931220800010",
    "20008050500015",
    "19931222400017",
    "19931448500012",
    "19931210900010",
    "19931211700013",
    "19931212500016",
    "19931209100010",
    "19931213300028",
    "20004548200011",
    "19930586300011",
    "19931978100019",
    "19931191100010",
    "19930616800014",
    "19932233000010",
    "19931497200019",
    "19930897400013",
    "19931221600013",
    "19931192900012",
    "19931546600011",
    "19932038300011",
    "19931382600018",
    "19932225600017",
    "19931194500018",
    "19931883300027",
    "19931196000025",
    "19931005300012",
    "19931723100017",
    "19931612600010",
    "19931218200017",
    "19931216600010",
    "19931217400014",
    "19931788400013",
    "20008799700017",
    "19931860100010",
    "19931199400024",
    "19932227200022",
    "19931200000029",
    "19930611900025",
    "20008800300013",
    "19931204200013",
    "19931429500015",
    "19931184600018",
    "20004549000014",
    "20008048900012",
    "19931185300014",
    "19931433700015",
    "21590527400084",
    "26760171400020",
    "26270874600215",
    "20004943500015",
    "39381721800018",
    "26710001400047",
    "26710061800029",
    "77556776100041",
    "26710130100021",
    "19550024400015",
    "19550804900010",
    "19550018600018",
    "19550014500014",
    "19550011100024",
    "19550840300019",
    "19550007900015",
    "19550848600014",
    "21920022700011",
    "21420096600015",
    "77757176100082",
    "77562228500275",
    "26490003600015",
    "21790202200011",
    "26760248000027",
    "19861073500013",
    "19861072700010",
    "19861071900017",
    "19861053700013",
    "19861038800011",
    "19860984400016",
    "19860876200011",
    "19860799600024",
    "19860792100014",
    "19860791300011",
    "19860723600017",
    "19860702000015",
    "19860053800013",
    "19860049600014",
    "19860047000019",
    "19860046200016",
    "19860045400013",
    "19860044700017",
    "19860043900014",
    "19860040500015",
    "19860032200012",
    "19860027200019",
    "19860026400016",
    "19860023100015",
    "19860020700015",
    "19860019900014",
    "19860017300019",
    "19860016500015",
    "19860015700012",
    "19860014000018",
    "19860002500011",
    "21170414300059",
    "25660087500049",
    "43842088700103",
    "26310060400010",
    "26590680000015",
    "21780646200586",
    "21780646200644",
    "21780646200594",
    "21780646200735",
    "21780646200651",
    "21780646200677",
    "21780646200685",
    "21780646200669",
    "21780646200693",
    "21780646200701",
    "21780646200628",
    "21780646200727",
    "21780646200636",
    "21780646200560",
    "21780646200719",
    "21780646200453",
    "21780646200354",
    "21780646200479",
    "21780646200289",
    "21780646200180",
    "21780646200271",
    "21780646200172",
    "21780646200099",
    "21780646200552",
    "21780646200396",
    "21780646200503",
    "21780646200081",
    "21780646200149",
    "21780646200404",
    "21780646200131",
    "21780646200461",
    "21780646200339",
    "21780646200370",
    "21780646200198",
    "21780646200388",
    "21780646200545",
    "21780646200206",
    "21780646200164",
    "21780646200511",
    "21780646200073",
    "21780646200297",
    "21780646200321",
    "21780646200214",
    "21780646200107",
    "21780646200230",
    "21780646200420",
    "21780646200156",
    "21780646200123",
    "34480930600014",
    "20003070800032",
    "20002309100016",
    "19622791200017",
    "19620097600013",
    "19622790400014",
    "19622434900015",
    "19622874600018",
    "19620123000014",
    "19623312600024",
    "19622299600015",
]


# we disable post_save signals to avoid calling fill_geo_fields_from_siret
# Note: this will also disable history tracking (on creation)
@factory.django.mute_signals(post_save)
class CanteenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Canteen
        skip_postgeneration_save = True

    name = factory.Faker("text", max_nb_chars=20)
    # siret: empty if groupe
    siret = factory.LazyAttributeSequence(
        lambda obj, n: SIRET_LIST_FOR_FACTORY[n % len(SIRET_LIST_FOR_FACTORY)]
        if obj.production_type != Canteen.ProductionType.GROUPE
        else None
    )
    # siren_unite_legale: filled if groupe
    siren_unite_legale = factory.LazyAttributeSequence(
        lambda obj, n: SIRET_LIST_FOR_FACTORY[n % len(SIRET_LIST_FOR_FACTORY)][:9]
        if obj.production_type == Canteen.ProductionType.GROUPE
        else None
    )
    # city & city_insee_code
    city = factory.LazyAttribute(
        lambda obj: factory.Faker("city") if obj.production_type != Canteen.ProductionType.GROUPE else None
    )
    city_insee_code = factory.LazyAttribute(
        lambda obj: factory.Faker("postcode") if obj.production_type != Canteen.ProductionType.GROUPE else None
    )
    daily_meal_count = 12
    yearly_meal_count = 1000
    management_type = random.choice(Canteen.ManagementType.values)
    production_type = Canteen.ProductionType.ON_SITE  # the production_type with the least constraints
    # economic_model: empty if groupe
    economic_model = factory.LazyAttribute(
        lambda obj: Canteen.EconomicModel.PRIVATE if obj.production_type != Canteen.ProductionType.GROUPE else None
    )
    # sector_list: empty if groupe or central
    sector_list = factory.LazyAttribute(
        lambda obj: [Sector.SANTE_HOPITAL]
        if obj.production_type
        not in [
            Canteen.ProductionType.GROUPE,
            Canteen.ProductionType.CENTRAL,
        ]
        else []
    )

    @factory.post_generation
    def sectors_m2m(self, create, extracted, **kwargs):
        if not create or extracted == []:
            return
        if extracted:
            for sector in extracted:
                self.sectors_m2m.add(sector)
        else:
            for _ in range(random.randint(1, 3)):
                self.sectors_m2m.add(SectorM2MFactory())

    @factory.post_generation
    def managers(self, create, extracted, **kwargs):
        if not create or extracted == []:
            return
        if extracted:
            for manager in extracted:
                self.managers.add(manager)
        else:
            for _ in range(random.randint(1, 2)):
                self.managers.add(UserFactory())
