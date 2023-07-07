<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'DiagnosticsImporter' } }]" :title="type.title" />

    <v-row class="my-4 mx-0">
      <v-icon large class="mr-4" color="black">{{ type.icon }}</v-icon>
      <h1>{{ type.title }}</h1>
      <p v-if="type.description">{{ type.description }}</p>
    </v-row>
    <h2 class="my-4">1. Préparer le fichier</h2>
    <p>
      <a href="#documentation">
        Voir les données requises pour
        <b>{{ importDocString }}</b>
        .
      </a>
    </p>
    <DownloadLinkList
      groupTitle="On met à votre disposition un fichier exemple avec les données en bon format"
      :links="downloadLinks"
    />

    <!-- TODO: for now hide if COMPLETE -->
    <DsfrCallout v-if="isStaff" class="body-2 my-4">
      En tant que membre de l'équipe ma cantine, vous pouvez ajoter trois colonnes additionnelles à la fin du fichier
      CSV :
      <br />
      <ul>
        <li>Une liste d'adresses email de gestionnaires qui seront ajoutés sans être notifiés par email, et</li>
        <li>Un identifiant décrivant la source de données</li>
        <li>
          Optionnel : Un état de publication (les options sont
          <code>published</code>
          ou
          <code>draft</code>
          )
        </li>
        <li>
          Optionnel : Un état de télédéclaration (les options sont
          <code>teledeclared</code>
          , ou vide)
        </li>
      </ul>
      Téléchargez l'en-tête en format :
      <a class="text-decoration-underline" href="/static/documents/fichier_exemple_staff.xlsx" download>
        Excel (.xlsx)
      </a>
      ,
      <a class="text-decoration-underline" href="/static/documents/fichier_exemple_staff.csv" download>
        CSV
      </a>
      ,
      <a class="text-decoration-underline" href="/static/documents/fichier_exemple_staff.ods" download>
        OpenDocument (.ods)
      </a>
      <br />
      À noter que vous ne serez pas ajouté.e.s automatiquement à l'équipe de gestion sauf si votre mail se trouve dans
      une des colonnes de listes de gestionnaires.
      <br />
      Bon courage ! 👾 🚀
    </DsfrCallout>

    <h2 class="mt-8">2. Transfèrer le fichier</h2>
    <FileDrop
      v-model="file"
      subtitle="Format CSV encodé en UTF-8 attendu"
      :acceptTypes="['.csv', 'text/csv', '.tsv', 'text/tsv']"
      maxSize="10485760"
      @upload="upload"
      :disabled="importInProgress"
    />

    <v-card outlined class="pa-4" v-if="importInProgress">
      <v-progress-circular indeterminate color="primary" size="28" class="mr-4"></v-progress-circular>
      <span class="mt-1">Traitement en cours...</span>
    </v-card>
    <div v-if="!isNaN(canteenCount) && !importInProgress">
      <!-- TODO: maybe just redirect to mes cantines on success ? -->
      <div v-if="canteenCount > 0">
        <v-alert type="success" outlined>
          <span class="grey--text text--darken-4 body-2">
            {{ canteenCount }} cantines
            <span v-if="diagnosticCount">et {{ diagnosticCount }} diagnostics&nbsp;</span>
            <span v-if="teledeclarationCount">et {{ teledeclarationCount }} télédéclarations&nbsp;</span>
            <span>ont été {{ diagnosticCount ? "traités" : "traitées" }}.</span>
          </span>
        </v-alert>
        <router-link :to="{ name: 'ManagementPage' }" class="ma-4">← Retourner à mes cantines</router-link>
      </div>
      <div v-if="errors && errors.length">
        <h2 class="my-4">3. Adresser les erreurs suivants, et re-essayer</h2>
        <p class="text-body-2 red--text text--darken-4" v-if="canteenCount === 0">
          Nous n'avons pas pu traiter votre fichier. Vous trouverez ci-dessous des informations sur les erreurs
          rencontrées.
        </p>
        <p class="text-body-2">
          Revoir
          <a href="#documentation">notre documentation</a>
          pour repondre aux questions les plus fréquentes, ou
          <a href="#contact">contactez-nous</a>
          pour plus d'aide.
        </p>
        <v-alert type="error" outlined>
          <v-simple-table color="red darken-2" dense>
            <template v-slot:default>
              <thead>
                <tr>
                  <th>Ligne</th>
                  <th>Erreur</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="error in errors" :key="error.row">
                  <td>{{ error.row }}</td>
                  <td>{{ error.message }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-alert>
      </div>
    </div>

    <v-divider class="my-8" />

    <h2 class="my-4" id="documentation">Le détail</h2>
    <v-card
      :class="{ 'd-flex': true, 'flex-column': $vuetify.breakpoint.xs, 'align-center': $vuetify.breakpoint.xs }"
      outlined
    >
      <video
        ref="video"
        class="ma-4"
        :style="`max-width: ${$vuetify.breakpoint.xs ? '70%' : '30%'}; background: #333; border-radius: 10px`"
        poster="/static/images/video-poster-import-masse.webp"
        controls
      >
        <source
          type="video/mp4"
          src="https://cellar-c2.services.clever-cloud.com/ma-cantine-egalim/videos/Tutoriel-import-de-masse.m4v"
        />
        Votre navigateur ne peut pas afficher des vidéos.
      </video>

      <div>
        <p class="ma-4">
          Régardez notre vidéo tutorial pour repondre aux questions les plus fréquentes.
          <br />
          <br />
          Si vous avez toujours des questions ou des problèmes, n'hésitez pas à nous contacter à
          <a href="mailto:support-egalim@beta.gouv.fr">support-egalim@beta.gouv.fr</a>
          .
        </p>
      </div>
    </v-card>
    <h3 class="my-6">Format du fichier</h3>
    <p>
      Le fichier CSV doit être encodé avec UTF-8 et contenir un diagnostic par ligne. Chaque ligne doit aussi inclure
      les informations de la cantine associée.
    </p>
    <p>Les données doivent être présentées dans l'ordre indiqué ci-dessous.</p>
    <p>Si un diagnostic pour la même année et la même cantine existe déjà il ne sera pas modifié.</p>
    <h4 class="my-6">Colonnes</h4>
    <v-simple-table class="my-6">
      <template v-slot:default>
        <thead>
          <tr>
            <th>Colonne</th>
            <th>Champ</th>
            <th>Description</th>
            <th>Type</th>
            <th>Exemple</th>
            <th>Obligatoire</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(field, idx) in sharedDocumentation" :key="idx">
            <td class="text-center">{{ idx + 1 }}</td>
            <td>{{ field.name }}</td>
            <td v-html="field.description"></td>
            <td>{{ field.type }}</td>
            <td style="min-width: 160px;">{{ field.example }}</td>
            <td class="text-center">{{ field.optional ? "✘" : "✔" }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
    <p>
      Les champs suivants concernent les données d'approvisionnement.
    </p>
    <v-simple-table class="my-2" v-if="diagnosticDocumentation.length">
      <template v-slot:default>
        <thead>
          <tr>
            <th>Colonne</th>
            <th>Champ</th>
            <th>Description</th>
            <th>Type</th>
            <th>Exemple</th>
            <th>Obligatoire</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(field, idx) in diagnosticDocumentation" :key="idx">
            <td class="text-center">{{ sharedDocumentation.length + idx + 1 }}</td>
            <td>{{ field.name }}</td>
            <td v-html="field.description"></td>
            <td>{{ field.type }}</td>
            <td>{{ field.example }}</td>
            <td class="text-center">{{ field.optional ? "✘" : "✔" }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
    <p v-else>Rien d'autre colonnes requises.</p>

    <DownloadLinkList
      groupTitle="On met à votre disposition un fichier exemple avec les données en bon format"
      :links="downloadLinks"
    />

    <HelpForm />
  </div>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav.vue"
import FileDrop from "@/components/FileDrop"
import HelpForm from "./HelpForm"
import Constants from "@/constants"
import DownloadLinkList from "@/components/DownloadLinkList.vue"
import DsfrCallout from "@/components/DsfrCallout"

export default {
  name: "DiagnosticImportPage",
  components: { BreadcrumbsNav, FileDrop, HelpForm, DownloadLinkList, DsfrCallout },
  props: ["importUrlSlug"],
  data() {
    const user = this.$store.state.loggedUser
    const importLevels = Constants.DiagnosticImportLevels.concat(Constants.CentralKitchenImportLevels)
    return {
      importLevels,
      importLevel: importLevels.find((x) => x.urlSlug === this.importUrlSlug)["key"],
      file: undefined,
      canteens: undefined,
      canteenCount: undefined,
      diagnosticCount: undefined,
      teledeclarationCount: undefined,
      errors: undefined,
      seconds: undefined,
      importInProgress: false,
      sharedDocumentation: [
        {
          name: "SIRET de l'établissement",
          description: "Ce SIRET doit être unique car il correspond à un lieu physique.",
          type: "14 chiffres, avec ou sans espaces",
          example: "000 000 000 00000",
        },
        {
          name: "Nom de l'établissement",
          example: "Ma Cantine",
          type: "Texte libre",
        },
        {
          name: "Code géographique INSEE de la ville",
          example: "69123",
          optional: true,
        },
        {
          name: "Code postal",
          description: "En cas d'absence de code INSEE, ce champ devient obligatoire.",
          example: "69001",
          optional: true,
        },
        {
          name: "SIRET de la cantine distributrice ou SRC",
          description:
            "Ce SIRET peut être vide ou utilisé pour plusieurs lignes, dans le cas où c'est le gestionnaire de la SRC ou de la cuisine centrale qui remplit les lignes pour chaque cuisine-site/satellite.",
          type: "14 chiffres, avec ou sans espaces",
          example: "999 999 999 99999",
          optional: true,
        },
        {
          name: "Nombre de repas servis par jour",
          type: "Chiffre",
          example: "300",
        },
        {
          name: "Nombre total de couverts à l'année",
          type: "Chiffre",
          description: "Y compris les couverts livrés",
          example: "67000",
        },
        {
          name: "Secteurs",
          description: `Options acceptées : ${this.$store.state.sectors.map(
            (x) => " <code>" + x.name + "</code>"
          )}. Spécifiez plusieurs en séparant avec un <code>+</code>.`,
          type: "Texte (choix unique)",
          example: `${this.$store.state.sectors[0].name}+${this.$store.state.sectors[1].name}`,
        },
        {
          name: "Mode de production",
          description:
            "Le mode de production de votre cantine. Les options :<br />- <code>central</code> si vous êtes une cuisine centrale sans lieu de consommation<br/>- <code>central_serving</code> si vous êtes une cuisine centrale qui accueille aussi des convives sur place,<br/>- <code>site</code> si vous êtes une cantine qui produit les repas sur place, et<br/>- <code>site_cooked_elsewhere</code> si vous êtes une cantine qui sert des repas preparés par une cuisine centrale.<br/>",
          type: "Texte (choix unique)",
          example: "central",
        },
        {
          name: "Mode de gestion",
          description:
            "Comment le service des repas est géré. Options acceptées : <code>direct</code> (directe) et <code>conceded</code> (concédé).",
          type: "Texte (choix unique)",
          example: "direct",
        },
        {
          name: "Secteur économique",
          description:
            "Le type d'établissement. Options acceptées : <code>public</code> et <code>private</code> (privé).",
          type: "Texte (choix unique)",
          example: "public",
          optional: true,
        },
        {
          name: "Gestionnaires additionnels (adresses emails)",
          description:
            "Les personnes avec ces adresses seront considérées comme gestionnaires de la cantine et pourront modifier toutes ses données.",
          type: "Texte (adresses email séparées par une virgule)",
          example: "gestionnaire1@example.com, gestionnaire2@example.com",
          optional: true,
        },
      ],
      isStaff: user.isStaff,
    }
  },
  computed: {
    type() {
      return this.importLevels.find((level) => level.key === this.importLevel)
    },
    diagnosticDocumentation() {
      if (this.importLevel === "NONE") return []
      const numberFormatExample = "En format <code>1234</code>/<code>1234.5</code>/<code>1234.56</code>."
      const simpleValues = [
        "Valeur d'achats bio HT",
        "Valeur d'achats SIQO (hors bio) HT",
        "Valeur (en HT) de mes achats prenant en compte les coûts imputés aux externalités environnementales ou acquis sur la base de leurs performances en matière environnementale",
        "Valeur (en HT) des autres achats EGAlim",
        "Valeur (en HT) des mes achats en viandes et volailles fraiches ou surgelées total",
        "Valeur (en HT) des mes achats EGAlim en viandes et volailles fraiches ou surgelées",
        "Valeur (en HT) des mes achats provenance France en viandes et volailles fraiches ou surgelées",
        "Valeur (en HT) des mes achats en poissons, produits de la mer et de l'aquaculture total",
        "Valeur (en HT) des mes achats EGAlim en poissons, produits de la mer et de l'aquaculture",
      ]
      let valuesArray = simpleValues
      const array = [
        {
          name: "Année du diagnostic",
          description: "En format <code>YYYY</code>.",
          type: "Chiffre",
          example: "2020",
        },
        {
          name: "Valeur totale d'achats HT",
          description: numberFormatExample,
          type: "Chiffre",
          example: "1234.99",
        },
      ]
      if (this.importLevel === "COMPLETE") {
        valuesArray = [
          "La valeur (en HT) des mes achats en viandes et volailles fraiches ou surgelées total",
          "La valeur (en HT) des mes achats en poissons, produits de la mer et de l'aquaculture total",
          "Bio : Viandes et volailles fraîches et surgelées",
          "Bio : Produits aquatiques frais et surgelés",
          "Bio : Fruits et légumes frais et surgelés",
          "Bio : Charcuterie",
          "Bio : BOF (Produits laitiers, beurre et œufs)",
          "Bio : Boulangerie/Pâtisserie fraîches",
          "Bio : Boissons",
          "Bio : Autres produits frais, surgelés et d’épicerie",
          "Label rouge : Viandes et volailles fraîches et surgelées",
          "Label rouge : Produits aquatiques frais et surgelés",
          "Label rouge : Fruits et légumes frais et surgelés",
          "Label rouge : Charcuterie",
          "Label rouge : BOF (Produits laitiers, beurre et œufs)",
          "Label rouge : Boulangerie/Pâtisserie fraîches",
          "Label rouge : Boissons",
          "Label rouge : Autres produits frais, surgelés et d’épicerie",
          "AOC / AOP / IGP / STG : Viandes et volailles fraîches et surgelées",
          "AOC / AOP / IGP / STG : Produits aquatiques frais et surgelés",
          "AOC / AOP / IGP / STG : Fruits et légumes frais et surgelés",
          "AOC / AOP / IGP / STG : Charcuterie",
          "AOC / AOP / IGP / STG : BOF (Produits laitiers, beurre et œufs)",
          "AOC / AOP / IGP / STG : Boulangerie/Pâtisserie fraîches",
          "AOC / AOP / IGP / STG : Boissons",
          "AOC / AOP / IGP / STG : Autres produits frais, surgelés et d’épicerie",
          "Certification environnementale de niveau 2 ou HVE : Viandes et volailles fraîches et surgelées",
          "Certification environnementale de niveau 2 ou HVE : Produits aquatiques frais et surgelés",
          "Certification environnementale de niveau 2 ou HVE : Fruits et légumes frais et surgelés",
          "Certification environnementale de niveau 2 ou HVE : Charcuterie",
          "Certification environnementale de niveau 2 ou HVE : BOF (Produits laitiers, beurre et œufs)",
          "Certification environnementale de niveau 2 ou HVE : Boulangerie/Pâtisserie fraîches",
          "Certification environnementale de niveau 2 ou HVE : Boissons",
          "Certification environnementale de niveau 2 ou HVE : Autres produits frais, surgelés et d’épicerie",
          "Pêche durable : Viandes et volailles fraîches et surgelées",
          "Pêche durable : Produits aquatiques frais et surgelés",
          "Pêche durable : Fruits et légumes frais et surgelés",
          "Pêche durable : Charcuterie",
          "Pêche durable : BOF (Produits laitiers, beurre et œufs)",
          "Pêche durable : Boulangerie/Pâtisserie fraîches",
          "Pêche durable : Boissons",
          "Pêche durable : Autres produits frais, surgelés et d’épicerie",
          "Région ultrapériphérique : Viandes et volailles fraîches et surgelées",
          "Région ultrapériphérique : Produits aquatiques frais et surgelés",
          "Région ultrapériphérique : Fruits et légumes frais et surgelés",
          "Région ultrapériphérique : Charcuterie",
          "Région ultrapériphérique : BOF (Produits laitiers, beurre et œufs)",
          "Région ultrapériphérique : Boulangerie/Pâtisserie fraîches",
          "Région ultrapériphérique : Boissons",
          "Région ultrapériphérique : Autres produits frais, surgelés et d’épicerie",
          "Commerce équitable : Viandes et volailles fraîches et surgelées",
          "Commerce équitable : Produits aquatiques frais et surgelés",
          "Commerce équitable : Fruits et légumes frais et surgelés",
          "Commerce équitable : Charcuterie",
          "Commerce équitable : BOF (Produits laitiers, beurre et œufs)",
          "Commerce équitable : Boulangerie/Pâtisserie fraîches",
          "Commerce équitable : Boissons",
          "Commerce équitable : Autres produits frais, surgelés et d’épicerie",
          "Fermier : Viandes et volailles fraîches et surgelées",
          "Fermier : Produits aquatiques frais et surgelés",
          "Fermier : Fruits et légumes frais et surgelés",
          "Fermier : Charcuterie",
          "Fermier : BOF (Produits laitiers, beurre et œufs)",
          "Fermier : Boulangerie/Pâtisserie fraîches",
          "Fermier : Boissons",
          "Fermier : Autres produits frais, surgelés et d’épicerie",
          "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie : Viandes et volailles fraîches et surgelées",
          "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie : Produits aquatiques frais et surgelés",
          "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie : Fruits et légumes frais et surgelés",
          "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie : Charcuterie",
          "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie : BOF (Produits laitiers, beurre et œufs)",
          "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie : Boulangerie/Pâtisserie fraîches",
          "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie : Boissons",
          "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie : Autres produits frais, surgelés et d’épicerie",
          "Produits acquis sur la base de leurs performances en matière environnementale : Viandes et volailles fraîches et surgelées",
          "Produits acquis sur la base de leurs performances en matière environnementale : Produits aquatiques frais et surgelés",
          "Produits acquis sur la base de leurs performances en matière environnementale : Fruits et légumes frais et surgelés",
          "Produits acquis sur la base de leurs performances en matière environnementale : Charcuterie",
          "Produits acquis sur la base de leurs performances en matière environnementale : BOF (Produits laitiers, beurre et œufs)",
          "Produits acquis sur la base de leurs performances en matière environnementale : Boulangerie/Pâtisserie fraîches",
          "Produits acquis sur la base de leurs performances en matière environnementale : Boissons",
          "Produits acquis sur la base de leurs performances en matière environnementale : Autres produits frais, surgelés et d’épicerie",
          "Non-Egalim : Viandes et volailles fraîches et surgelées",
          "Non-Egalim : Produits aquatiques frais et surgelés",
          "Non-Egalim : Fruits et légumes frais et surgelés",
          "Non-Egalim : Charcuterie",
          "Non-Egalim : BOF (Produits laitiers, beurre et œufs)",
          "Non-Egalim : Boulangerie/Pâtisserie fraîches",
          "Non-Egalim : Boissons",
          "Non-Egalim : Autres produits frais, surgelés et d’épicerie",
          "Provenance France : Viandes et volailles fraîches et surgelées",
          "Provenance France : Produits aquatiques frais et surgelés",
          "Provenance France : Fruits et légumes frais et surgelés",
          "Provenance France : Charcuterie",
          "Provenance France : BOF (Produits laitiers, beurre et œufs)",
          "Provenance France : Boulangerie/Pâtisserie fraîches",
          "Provenance France : Boissons",
          "Provenance France : Autres produits frais, surgelés et d’épicerie",
          "Circuit-court : Viandes et volailles fraîches et surgelées",
          "Circuit-court : Produits aquatiques frais et surgelés",
          "Circuit-court : Fruits et légumes frais et surgelés",
          "Circuit-court : Charcuterie",
          "Circuit-court : BOF (Produits laitiers, beurre et œufs)",
          "Circuit-court : Boulangerie/Pâtisserie fraîches",
          "Circuit-court : Boissons",
          "Circuit-court : Autres produits frais, surgelés et d’épicerie",
          "Produit local : Viandes et volailles fraîches et surgelées",
          "Produit local : Produits aquatiques frais et surgelés",
          "Produit local : Fruits et légumes frais et surgelés",
          "Produit local : Charcuterie",
          "Produit local : BOF (Produits laitiers, beurre et œufs)",
          "Produit local : Boulangerie/Pâtisserie fraîches",
          "Produit local : Boissons",
          "Produit local : Autres produits frais, surgelés et d’épicerie",
        ]
      }
      valuesArray.forEach((value) => {
        array.push({
          name: value,
          description: numberFormatExample,
          type: "Chiffre",
          example: "1234.99",
          optional: true,
        })
      })
      return array
    },
    downloadLinks() {
      const labels = {
        xlsx: "Excel",
        ods: "OpenDocument",
        csv: "CSV",
      }
      const importSizes = {
        CC_COMPLETE: {
          csv: "UNKNOWN ko",
          ods: "UNKNOWN Ko",
          xlsx: "UNKNOWN Ko",
        },
        CC_SIMPLE: {
          csv: "UNKNOWN ko",
          ods: "UNKNOWN Ko",
          xlsx: "UNKNOWN Ko",
        },
        COMPLETE: {
          csv: "5 Ko",
          ods: "15 Ko",
          xlsx: "13 Ko",
        },
        SIMPLE: {
          csv: "771 o",
          ods: "11 Ko",
          xlsx: "11 Ko",
        },
        NONE: {
          csv: "321 o",
          ods: "10 Ko",
          xlsx: "6 Ko",
        },
      }
      let filename = "/static/documents/"
      if (this.importLevel === "COMPLETE") filename = filename + "fichier_exemple_complet_ma_cantine"
      else if (this.importLevel === "NONE") filename = filename + "fichier_exemple_ma_cantine_no_diag"
      else filename = filename + "fichier_exemple_ma_cantine"
      return ["xlsx", "ods", "csv"].map((fileType) => ({
        href: `${filename}.${fileType}`,
        label: `Télécharger le fichier exemple en format ${labels[fileType]}`,
        sizeStr: importSizes[this.importLevel][fileType],
      }))
    },
    importDocString() {
      return {
        SIMPLE: "l'import simple",
        COMPLETE: "l'import complet",
        NONE: "l'import de cantines seulement",
        CC_SIMPLE: "la mise à jour des satellites et l'import simple",
        CC_COMPLETE: "la mise à jour des satellites et l'import complet",
      }[this.importLevel]
    },
  },
  created() {
    document.title = `${this.type.title} - Importer des diagnostics - ${this.$store.state.pageTitleSuffix}`
  },
  methods: {
    upload() {
      this.importInProgress = true
      this.$store
        .dispatch("importDiagnostics", {
          importLevel: this.importLevel,
          payload: { file: this.file },
        })
        .then((json) => {
          this.importInProgress = false
          this.file = null
          this.canteens = json.canteens
          this.canteenCount = json.canteens.length
          this.diagnosticCount = json.count
          this.teledeclarationCount = json.teledeclarations
          this.errors = json.errors
          this.seconds = json.seconds
          let resultMessage = {
            message: `${this.canteenCount} cantines traitées`,
            status: "success",
          }
          if (this.errors.length) {
            resultMessage.title = "Echec d'import"
            resultMessage.message = "Merci de vérifier les erreurs détaillés et de réessayer"
            resultMessage.status = "error"
          }
          this.$store.dispatch("notify", resultMessage)
          if (this.$matomo) {
            this.$matomo.trackEvent("inquiry", "send", "import-diagnostics-success")
          }
        })
        .catch((e) => {
          this.importInProgress = false
          this.$store.dispatch("notifyServerError", e)
        })
    },
  },
  beforeRouteEnter(to, from, next) {
    const importLevels = Constants.DiagnosticImportLevels.concat(Constants.CentralKitchenImportLevels)
    const legacyUrlKeys = importLevels.map((x) => ({ key: x.key, slug: x.urlSlug }))
    for (let i = 0; i < legacyUrlKeys.length; i++) {
      if (to.params.importUrlSlug === legacyUrlKeys[i].key)
        return next({ name: "DiagnosticImportPage", params: { importUrlSlug: legacyUrlKeys[i].slug } })
    }

    if (importLevels.map((x) => x.urlSlug).indexOf(to.params.importUrlSlug) === -1) return next({ name: "NotFound" })

    return next()
  },
}
</script>
