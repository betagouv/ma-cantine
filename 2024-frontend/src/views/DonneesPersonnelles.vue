<script setup>
import { onMounted } from "vue"
import { showContent } from "@/services/matomo.js"
import AppRawHTML from "@/components/AppRawHTML.vue"
import LayoutOneColumn from "@/layouts/LayoutOneColumn.vue"

const linkCleverCloud =
  '<a href="https://www.clever-cloud.com/fr/conditions-generales-dutilisation/accord-de-traitement-des-donnees/"target="_blank">Lien vers le DPA</a>'

onMounted(() => {
  showContent()
})
</script>

<template>
  <LayoutOneColumn>
    <section>
      <h2>
        1 - Qui est responsable de traitement ?
      </h2>
      <p>
        Le responsable de l’utilisation des données est la Direction générale de l’alimentation du ministère de
        l’agriculture et de la souveraineté alimentaire, représentée par Madame Maud FAIPOUX, Directrice générale de
        l’Alimention.
      </p>
    </section>
    <section>
      <h2>
        2 - Pourquoi traitons-nous ces données ?
      </h2>
      <p>
        « ma cantine » traite des données à caractère personnel pour accompagner au mieux les acteurs de la restauration
        collective dans leur offre aux consommateurs pour une alimentation de qualité, saine et durable.
      </p>
      <p>
        Cette plateforme permet ainsi :
      </p>
      <ul>
        <li>
          Une meilleure connaissance des lois EGalim via une description détaillée et pédagogique des mesures&nbsp;;
        </li>
        <li>
          Un aperçu de l'état des lieux des cantines ayant partagé leurs données pour connaître leur positionnement et
          éventuellement fomenter des échanges entre elles et avec leurs convives&nbsp;;
        </li>
        <li>
          Une option d'auto-diagnostic pour les acteurs de la restauration collective afin de s'auto-évaluer et accéder
          à des ressources pour s'améliorer&nbsp;;
        </li>
        <li>
          De créer un PDF à afficher ou à envoyer par mail à aux convives pour les informer sur les initiatives et la
          composition des repas servis&nbsp;;
        </li>
        <li>
          De répondre à leurs obligations réglementaires de télédéclaration de leurs données d’achat, à
          l’administration, lors des campagnes officielles annuelles.
        </li>
      </ul>
      <p>L’autodiagnostic sur « ma cantine » est disponible sans création de compte.</p>
    </section>
    <section>
      <h2>3 - Quelles sont les données que nous traitons ?</h2>
      <p>
        Ma Cantine traite les données à caractère personnel suivantes :
      </p>
      <DsfrTable
        :headers="['Type de données', 'Description des données']"
        :rows="[
          {
            rowData: [
              'Création de compte',
              'Certaines données sont obligatoires pour la création du compte : nom, prénom, nom d\'utilisateur, adresse électronique et numéro de téléphone. L’utilisateur doit également fournir un ensemble de données relatives à l’établissement concerné (SIRET, nombre de repas, nom de la cantine, ville, type de structure, mode de gestion etc…), qui ne sont pas considérées comme des données à caractère personnel.',
            ],
          },
          {
            rowData: [
              'Contact',
              'Sont collectées lors de la prise de contact avec les cantines l’adresse-mail et, de manière facultative, le prénom et le nom de la personne.',
            ],
          },
          {
            rowData: [
              'Inscription à une infolettre (newsletter)',
              'Adresse électronique de la personne qui souhaite recevoir l’infolettre.',
            ],
          },
          {
            rowData: ['Cookies', 'Traceurs destinés à améliorer la navigation sur la plateforme.'],
          },
        ]"
      />
    </section>

    <section>
      <h2>4 - Qu’est-ce qui nous autorise à traiter ces données ?</h2>
      <p>
        « ma cantine » traite des données à caractère personnel en se basant sur :
      </p>
      <ul>
        <li>
          L’exécution d’une mission d’intérêt public ou relevant de l’exercice de l’autorité publique dont est investi
          le responsable de traitement au sens de l’article 6-1 e du RPGD.
        </li>
        <li>
          Cette mission d’intérêt public consiste en la mise en œuvre des obligations prévues par les articles L. 230-5
          à L. 230-5-2 du code rural et de la pêche maritime mais également des articles R. 230-30-4 du même code et de
          l’arrêté du 14 septembre 2022 fixant les modalités de transmission par les gestionnaires de restaurants
          collectifs des données nécessaires à l'établissement du bilan statistique annuel mentionné au V de l'article
          L. 230-5-1 du code rural et de la pêche maritime.
        </li>
      </ul>
    </section>

    <section>
      <h2>5 - Pendant combien de temps conservons-nous ces données ?</h2>

      <DsfrTable
        :headers="['Type de données', 'Durée de la conservation']"
        :rows="[
          {
            rowData: [
              'Données relatives à la création d’un compte',
              '4 ans à compter de la dernière utilisation du compte',
            ],
          },
          { rowData: ['Données de contact', '4 ans à compter de la dernière prise de contact'] },
          {
            rowData: [
              'Données relatives à l’inscription à l’infolettre',
              'Jusqu’à la suppression du compte ou retrait du consentement',
            ],
          },
          { rowData: ['Cookies', 'Jusqu’au retrait du consentement ou 13 mois à compter du dépôt'] },
        ]"
      />
    </section>

    <section>
      <h2>6 - Quels droits avez-vous ?</h2>
      <p>Vous disposez :</p>
      <ul>
        <li>D’un droit d’information et d’un droit d’accès à vos données&nbsp;;</li>
        <li>D’un droit de rectification&nbsp;;</li>
        <li>D’un droit d’opposition&nbsp;;</li>
        <li>D’un droit à la limitation du traitement.</li>
      </ul>
      <p>
        Pour les exercer, contactez-nous :
      </p>
      <ul>
        <li>
          par voie électronique à :
          <a href="mailto:support-egalim@beta.gouv.fr">support-egalim@beta.gouv.fr</a>
        </li>
        <li>
          par voie postale à :
          <address>
            MINISTÈRE DE L’AGRICULTURE
            <br />
            Direction Générale de l’Alimentation
            <br />
            251 Rue de Vaugirard, 75015 Paris
          </address>
        </li>
      </ul>
      <p>
        Puisque ce sont des droits personnels, nous ne traiterons votre demande que si nous sommes en mesure de vous
        identifier. Dans le cas où nous ne parvenons pas à vous identifier, nous pouvons être amenés à vous demander une
        preuve de votre identité.
      </p>
      <p>
        Pour vous aider dans votre démarche, vous trouverez un modèle de courrier élaboré par la CNIL ici :
        <a href="https://www.cnil.fr/fr/modele/courrier/exercer-son-droit-dacces" target="_blank">
          https://www.cnil.fr/fr/modele/courrier/exercer-son-droit-dacces
        </a>
      </p>
      <p>
        Nous nous engageons à vous répondre dans un délai raisonnable qui ne saurait dépasser 1 mois à compter de la
        réception de votre demande.
      </p>
    </section>

    <section>
      <h2>7 - Qui va avoir accès à ces données ?</h2>
      <p>
        Les accès aux données sont strictement encadrés et juridiquement justifiés. Les personnes suivantes vont avoir
        accès aux données :
      </p>
      <DsfrTable
        :headers="['Données', 'Destinataires']"
        :rows="[
          {
            rowData: [
              'Données relatives à la création d’un compte et données de contact',
              'Agents publics habilités du ministère de l’agriculture et de la souveraineté alimentaire',
            ],
          },
        ]"
      />
    </section>

    <section>
      <h2>8 - Quelles mesures de sécurité mettons-nous en place ?</h2>
      <p>Nous mettons en place plusieurs mesures pour sécuriser les données :</p>
      <ul>
        <li>Stockage des données en base de données&nbsp;;</li>
        <li>Cloisonnement des données&nbsp;;</li>
        <li>Mesures de traçabilité&nbsp;;</li>
        <li>Surveillance&nbsp;;</li>
        <li>Protection contre les virus, malwares et logiciels espions&nbsp;;</li>
        <li>Protection des réseaux&nbsp;;</li>
        <li>Sauvegarde&nbsp;;</li>
        <li>Mesures restrictives limitant l’accès physiques aux données à caractère personnel.</li>
      </ul>
    </section>

    <section>
      <h2>9 - Qui nous aide à traiter les données ?</h2>
      <p>
        Certaines des données sont envoyées à d’autres acteurs, appelés “sous-traitants de données”, pour qu’ils nous
        aident à les manipuler. Nous nous assurons qu’ils respectent strictement le RGPD et qu’ils apportent des
        garanties suffisantes en matière de sécurité.
      </p>
      <DsfrTable
        :headers="['Sous-traitant', 'Pays destinataire', 'Traitement réalisé', 'Garanties']"
        :rows="[
          { rowData: ['Clever Cloud', 'France', 'Hébergement', { component: AppRawHTML, html: linkCleverCloud }] },
        ]"
      />
    </section>

    <section>
      <h2 id="cookies">10 - Cookies</h2>
      <p>
        Un cookie est un fichier déposé sur votre terminal lors de la visite d’un site. Il a pour but de collecter des
        informations relatives à votre navigation et de vous adresser des services adaptés à votre terminal (ordinateur,
        mobile ou tablette).
      </p>
      <p>
        En application de l’article 5(3) de la directive 2002/58/CE modifiée concernant le traitement des données à
        caractère personnel et la protection de la vie privée dans le secteur des communications électroniques,
        transposée à l’article 82 de la loi n° 78-17 du 6 janvier 1978 relative à l’informatique, aux fichiers et aux
        libertés, les traceurs ou cookies suivent deux régimes distincts.
      </p>
      <p>
        Les cookies strictement nécessaires au service ou ayant pour finalité exclusive de faciliter la communication
        par voie électronique sont dispensés de consentement préalable au titre de l’article 82 de la loi n° 78-17 du 6
        janvier 1978.
      </p>
      <p>
        Les cookies n’étant pas strictement nécessaires au service ou n’ayant pas pour finalité exclusive de faciliter
        la communication par voie électronique doivent être consenti par l’utilisateur.
      </p>
      <p>
        Ce consentement de la personne concernée pour une ou plusieurs finalités spécifiques constitue une base légale
        au sens du RGPD et doit être entendu au sens de l'article 6-1 a) du RGPD et à la libre circulation des données.
      </p>
      <p>Cookies recensés sur Ma Cantine :</p>
      <DsfrTable
        :headers="['Site', 'Description', 'Autorisation']"
        :rows="[
          {
            rowData: [
              'Matomo',
              'Cookie de mesure d’audience, dans sa version exemptée de consentement préalable, telle que validée par la CNIL.',
              {
                component: AppRawHTML,
                html: '<div id=\'matomo-opt-out\'></div>',
              },
            ],
          },
          {
            rowData: [
              'Crisp',
              'Chatbot qui permet d’interagir avec les équipes de Ma Cantine pour toutes questions concernant la plateforme.',
              'Toujours actif.',
            ],
          },
        ]"
      />
      <p>
        À tout moment, vous pouvez refuser l’utilisation des cookies et désactiver le dépôt sur votre ordinateur en
        utilisant la fonction dédiée de votre navigateur (fonction disponible notamment sur Microsoft Internet Explorer
        11, Google Chrome, Mozilla Firefox, Apple Safari et Opera).
      </p>
      <p>
        Pour aller plus loin, vous pouvez consulter les fiches proposées par la Commission Nationale de l'Informatique
        et des Libertés (CNIL) :
      </p>
      <ul>
        <li>
          <a
            href="https://www.cnil.fr/fr/cookies-traceurs-que-dit-la-loi"
            target="_blank"
            title="Cookies & traceurs : que dit la loi ? - ouvre une nouvelle fenêtre"
          >
            Cookies & traceurs : que dit la loi ?
          </a>
        </li>
        <li>
          <a
            href="https://www.cnil.fr/fr/cookies-les-outils-pour-les-maitriser"
            target="_blank"
            title="Cookies : les outils pour les maîtriser - ouvre une nouvelle fenêtre"
          >
            Cookies : les outils pour les maîtriser
          </a>
        </li>
      </ul>
    </section>
  </LayoutOneColumn>
</template>
