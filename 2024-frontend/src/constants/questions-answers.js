const groups = [
  {
    title: "La plateforme",
    accordions: [
      {
        answer:
          "« ma cantine » est un service numérique opéré par le Ministère en charge de l’agriculture (MASA) avec l’appui de la Direction Interministérielle du Numérique (DINUM). Son objectif est d'accompagner la transition alimentaire des services de restauration collective, les cantines vers une alimentation et une consommation plus durable. Cette plateforme est à la fois un outil d’accompagnement pour les gestionnaires, un outil d’information pour les convives citoyens et un outil de transmission d’information vers l’administration pour le suivi de cette transition.",
        question: "Qu'est-ce que « ma cantine » ?",
      },
    ],
  },
  {
    title: "Inscription",
    accordions: [
      {
        answer:
          "L’inscription des gestionnaires, responsables légaux d’un service de restauration (dans les secteurs public et privé) est obligatoire. Le décret du 23 avril 2019, pris en application de la loi EGalim du 30 octobre 2018, prévoit la réalisation d’un bilan statistique de la mise en œuvre des obligations prévues par la loi, sur la base des éléments transmis, dans des conditions fixées par l'arrêté ministériel du 14 septembre 2022. Ce dernier précise la nature des informations à déclarer et le moyen de le faire par « ma cantine ». La plateforme permet également de bénéficier d'un accompagnement à la mise en place des mesures réglementaires des lois EGalim et Climat et Résilience et de répondre aux obligations d’information des convives.",
        question: "L’inscription sur la plateforme est-elle obligatoire ?",
      },
      {
        answer:
          "ma cantine est destinée aux responsables légaux et aux gestionnaires publics et privés des services de restauration collective. Concrètement, il s'agit de plusieurs types de fonctions : Élu(e)s de collectivité, Directeur(trice) d’établissement, Gestionnaire administratif, Comptable, Responsable Restauration, Chef(fe) et ou cuisinier. Plusieurs personnes peuvent etre rattachées à une même cantine. Les services de restauration peuvent etre en gestion directe ou en gestion déléguée/concédée.",
        question: "Qui peut s’inscrire sur « ma cantine » ?",
      },
      {
        name: "HowToSignUp",
        question: "Comment s’inscrire sur « ma cantine » ?",
      },
      {
        answer:
          "C'est au gestionnaire de la collectivité ou du accordionsement de collectivités (EPCI, intercom, syndicats,...) de s'inscrire et de créer les établissements. Vous pouvez également demander à cette personne un accès gestionnaire sur ces établissements.",
        question:
          "Je représente une commune mais ne gère pas la restauration scolaire de celle-ci, suis-je concernée ?",
      },
      {
        answer:
          "Oui, vous êtes concerné. Dans le cas d’une gestion déléguée/concédée, si en tant que donneur d’ordre vous n'avez pas toutes les informations requises pour mettre à jour vos données d'achat dans « ma cantine », vous avez deux options: soit vous les demandez à votre prestataire et les renseignez dans votre espace cantine ; soit vous autorisez le prestataire à les saisir lui-même dans votre espace cantine. Dans ce cas, votre prestataire doit se créer un compte dans « ma cantine » et vous devez l'ajouter en gestionnaire de l'établissement.",
        question:
          "Je suis en gestion concédée/approvisionné par un restaurateur privé (société de restauration collective, traiteur, prestataire,...), suis-je concerné ?",
      },
      {
        answer:
          "Les restaurants « clients » doivent transmettre via « ma cantine » les informations sur leurs données d’achat. La possibilité est donnée à une SRC de pouvoir télétransmettre les données pour l’ensemble de ses restaurants « clients » (avec une possibilité de transmettre « en masse »). L’intérêt pour la SRC est de télétransmettre rapidement et simplement, et de pouvoir montrer, par la publication, les efforts et les résultats de son action. C’est aussi un service amené aux clients de la SRC qui n’auront pas cette action de télédéclaration à faire eux-mêmes. Cette décision de qui télédéclare entre la SRC et le client est à voir entre les deux parties.",
        question:
          "Quel intérêt pour une SRC (société de restauration collective) de saisir les informations des restaurants clients concernant les dispositions de la loi sur la plateforme « ma cantine » ?",
      },
      {
        answer:
          "Oui. Les gestionnaires de cuisines satellites peuvent se créer un compte et ajouter leur cantine, sauf si la cuisine centrale qui les dessert l’a déjà fait. Dans ce cas, je peux être gestionnaire additionnel de cet établissement, en demandant un accès à la cuisine centrale. A moyen terme, les cuisines satellites devront indiquer leurs propres données en matière d’approvisionnement.",
        question:
          "Je suis gestionnaire d'une cuisine satellite, suis-je concerné par l'inscription sur « ma cantine » ?",
      },
      {
        answer:
          "Les Départements et les Régions ont respectivement la compétence de la restauration collective pour les collèges et les lycées. Ils sont à ce titre sont responsables du référencement de leurs établissements sur « ma cantine ».  Une convention passée entre l'établissement et la collectivité territoriale de rattachement précise les modalités d'exercice de leurs compétences respectives. Elle comprend un volet relatif à la restauration scolaire, qui vise en particulier à répondre aux objectifs fixés par la loi EGalim (article L. 421-23 du code de l'éducation). La cantine peut être créée par l'une et/ou l'autre des parties et gérée par les deux.",
        question:
          "Je suis gestionnaire d'un collège ou d'un lycée, mon établissement a été créé, suis-je concerné par l'inscription dans « ma cantine » ?",
      },
      {
        answer:
          "Les gestionnaires de cuisines centrales doivent se créer un compte, créer leur cantine en déclarant chaque restaurant satellite qu’elles livrent. Jusqu'à la campagne 2024 de remontées des données de l'année civile 2023, les informations sur la mise en place des mesures EGalim peuvent être centralisées au niveau de la cuisine centrale. A moyen terme, les informations devront etre attribuées à chaque cuisines satellites.",
        question:
          "Je suis gestionnaire d'une cuisine centrale, suis-je concerné par l'inscription sur « ma cantine » ?",
      },
    ],
  },
  {
    title: "Création de mon établissement",
    accordions: [
      {
        component: "SiretRequired",
        question: "Le SIRET est-il obligatoire pour créer ma cantine ?",
      },
      {
        component: "NoSiret",
        question: "Comment faire si je ne dispose pas de SIRET pour créer mon établissement dans ma cantine ?",
      },
    ],
  },
  {
    title: "La loi",
    accordions: [
      {
        answer:
          "A ce jour, la loi ne prévoit pas de sanctions, ni de contrôles pour ce qui concerne l'atteinte des taux EGalim. Cependant la loi EGalim et plus récemment la Climat et Résilience, prévoient un renforcement de la transparence vis-à-vis des convives avec notamment l’obligation d’une information des convives sur leur lieu de repas, des objectifs atteints en matière de produits durables et de qualité entrant dans la composition des repas (Art. L. 230-5-3 du code rural) et d’une information des citoyens au travers un bilan statistique annuel de l’application de ces objectifs, remis au Parlement par le Gouvernement et rendu public (Article L. 230-5-1 du code rural).",
        question: "Comment sont vérifiées les obligations sur l’atteinte des taux EGalim en restauration collective ?",
      },
      {
        component: "ProviderObligation",
        question:
          "Mon prestataire ou délégataire refuse de me transmettre mes données d'achats. Quelles obligations pour lui ?",
      },
    ],
  },
  {
    title: "La mesure EGalim « qualité de produits »",
    accordions: [
      {
        answer:
          "A ce jour, pour les produits issus de la démarche Bleu-Blanc-Coeur ne bénéficiant pas d’un signe ou mention « officiel » listé par la loi EGalim, il est possible de les comptabiliser, comme pour tout autre produit, dans les objectifs de la loi EGalim à condition qu’ils soient sélectionnés à l’issue d’un processus de sélection ciblant « les produits acquis selon les modalités prenant en compte les coûts imputés aux externalités environnementales tout au long de son cycle de vie » ou « les produits dont l’acquisition a été fondée principalement sur la base de leurs performances en matière de protection de l’environnement et de développement des approvisionnements directs de produits de l’agriculture ». Le recours à ces modalités de sélection relève du libre choix et de la responsabilité de l’acheteur, dans le respect du code de la commande publique.",
        question: "Les produits Bleu-Blanc-Coeur (BBC) entrent-ils dans les 50 % de produits durables et de qualité ?",
      },
      {
        answer:
          "La catégorie citée par la loi EGalim est « Produits issus de la pêche maritime bénéficiant de l’écolabel Pêche durable ». Le label MSC (porté par l’ONG internationale MSC) est différent de la certification par l’écolabel « Pêche Durable ». Dans le cas où un fournisseur propose des produits labellisés « MSC pêche durable » en lieu et place de produits labellisés « écolabel Pêche durable, l’acheteur, sous sa propre responsabilité et sur la base d’éléments de preuve apportés par le fournisseur, peut étudier l’équivalence, dans le respect du code de la commande publique, de produits labellisés avec la catégorie écolabel « Pêche Durable ».",
        question:
          "Quels sont les produits issus de la « pêche durable » qui entrent dans les 50 % de produits durables et de qualité ?",
      },
      {
        answer:
          "Le code de la commande publique ne permet pas de faire mention directement de l’origine locale, ce qui serait contraire aux principes du droit de la concurrence. Ainsi, les produits « locaux » ne sont pas pris en compte dans l’objectif de 50 % de produits durables et de qualité, en tant que tels. Un produit local n’est comptabilisable que s’il entre dans une des catégories citées par la loi. Cependant, les guides d’achats, construits dans le cadre du Conseil National de la Restauration Collective, consultables sur « ma cantine », présentent des stratégies d’achats permettant de travailler sur des approvisionnements durables et de qualité, dans le cadre d’une démarche territoriale (notamment dans le cadre des projets alimentaires territoriaux).",
        question: "Quid des produits locaux ? Sont-ils pris en compte dans les 50% de produits « EGalim » ?",
      },
      {
        answer:
          "Pour un produit « origine France » ou acquis en « circuit court », il peut être comptabilisé s’il satisfait une des catégories définies dans la loi. Pour la catégorie « produit dont l’acquisition a été fondée principalement sur la base de leurs performances en matière de protection de l’environnement et de développement des approvisionnements directs de produits de l’agriculture », une expertise juridique est encore en cours, pour cadrer l’utilisation de ces critères de sélection. Le suivi des caractéristiques, produit « issu d’un circuit court » ou « d’origine française » est nécessaire pour l’établissement d’un bilan statistique annuel à remettre au Parlement chaque année. ",
        question: "Les produits « circuit court » et « origine France » sont-ils comptabilisables au titre des 50 % ?",
      },
    ],
  },
  {
    title: "Transmission des données par « ma cantine »",
    accordions: [
      {
        answer:
          "Le décret du 23 avril 2019, pris en application de la loi EGalim du 30 octobre 2018 précise que ces parts (taux EGalim) sont calculées à partir des valeurs d’achats HT des produits alimentaires. L’arrêté du 14 septembre 2022, indique que les informations à transmettre via « ma cantine » sont les valeurs d’achat (HT). Ces données permettent de réaliser le bilan statistique annuel.",
        question:
          "Pourquoi, dans mon diagnostic, fournir les valeurs d’achat et pas les parts (en %) des produits durables et de qualité, et de produits bio ?",
      },
      {
        answer:
          "Les données d'achat saisies dans « ma cantine » (dans le diagnostic) sont à télédéclarer tous les ans. Elles sont transmises à la DGAL (Direction générale de l’Alimentation) - ministère de l’Agriculture et de la Souveraineté Alimentaire (MASA) en vue d'etablir le bilan annuel à remettre au Parlement qui sera un document public.",
        question:
          "A qui les données relatives aux achats de denrées alimentaires déclarées dans « ma cantine » sont-elles fournies ? Pour quoi faire ?",
      },
      {
        answer:
          "Une API « ma cantine » est disponible pour les développeurs afin de se pouvoir s'interconnecter à la plateforme. La documentation est accessible pour les éditeurs de logiciel, il suffit de créer ou modifier votre profil en cochant le mode développeur.",
        question:
          "J'utilise un outil de suivi d'achats (type GPAO). Pourrais-je transmettre les données relatives aux achats automatiquement à partir de mon logiciel de suivi ?",
      },
      {
        answer:
          "« ma cantine » propose un outil de suivi de ses achats, gratuit, en ligne et qui permet de restituer ses informations dans un tableau de bord et de procéder simplement à la télédéclaration annuelle de ses achats. Pour l’utiliser il faut se créer un compte.",
        question: "Je ne dispose pas d’outil pour le suivi de mes achats comment faire ?",
      },
    ],
  },
]

export { groups }
