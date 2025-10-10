<template>
  <div class="text-left">
    <BreadcrumbsNav
      :links="[{ to: { name: 'ManagementPage' } }, { to: { name: 'GestionnaireImport' } }]"
      :title="type.title"
    />

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

    <DsfrCallout v-if="isStaff && staffImportAvailable" class="body-2 my-4">
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
      <a class="text-decoration-underline" href="/static/documents/fichier_exemple_staff.csv" download>
        CSV
      </a>
      <br />
      À noter que vous ne serez pas ajouté.e.s automatiquement à l'équipe de gestion sauf si votre mail se trouve dans
      une des colonnes de listes de gestionnaires.
      <br />
      Bon courage ! 👾 🚀
    </DsfrCallout>

    <h2 class="mt-8">2. Transférer le fichier</h2>
    <FileDrop
      v-model="file"
      subtitle="Format CSV attendu"
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
      <ImporterSuccessDialog
        v-if="canteenCount > 0 && !diagnosticCount && !teledeclarationCount"
        :isOpen="canteenCount > 0"
        :description="
          canteenCount > 1
            ? 'Vos cantines sont enregistrées et sont maintenant disponibles.'
            : 'Votre cantine est enregistrée et est maintenant disponible.'
        "
      />
      <ImporterSuccessDialog
        v-else-if="canteenCount > 0"
        :isOpen="canteenCount > 0"
        :description="
          canteenCount > 1
            ? 'Vos bilans sont enregistrés et sont maintenant disponibles.'
            : 'Votre bilan est enregistré et est maintenant disponible.'
        "
      />
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
        <p class="caption grey--text text--darken-3 mb-0">Encodage utilisé : {{ encodingUsed }}.</p>
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

    <v-divider aria-hidden="true" role="presentation" class="my-8" />

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
      Le fichier CSV doit commencer par une ligne en-tête avec le nom des colonnes exactement comme listé ci-dessous
      dans "Titre". Il doit ensuite contenir un bilan par ligne. Chaque ligne doit aussi inclure les informations de la
      cantine associée.
    </p>
    <p>Les données doivent être présentées dans l'ordre indiqué ci-dessous.</p>
    <p>Il n'est pas possible de modifier les bilans télédéclarés.</p>
    <h4 class="my-6">Colonnes</h4>
    <SchemaTable :schemaUrl="getDiagnosticSchemaUrl" />

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
import ImporterSuccessDialog from "@/components/ImporterSuccessDialog.vue"
import SchemaTable from "@/components/SchemaTable"

export default {
  name: "DiagnosticImportPage",
  components: { BreadcrumbsNav, FileDrop, HelpForm, DownloadLinkList, DsfrCallout, ImporterSuccessDialog, SchemaTable },
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
      encodingUsed: undefined,
      diagnosticSimpleSchemaUrl:
        "https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/main/data/schemas/imports/diagnostics.json",
      diagnosticCompleteSchemaUrl:
        "https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/main/data/schemas/imports/diagnostics_complets.json",
      diagnosticSimpleCCSchemaUrl:
        "https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/main/data/schemas/imports/diagnostics_cc.json",
      diagnosticCompleteCCSchemaUrl:
        "https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/main/data/schemas/imports/diagnostics_complets_cc.json",
      isStaff: user.isStaff,
    }
  },
  computed: {
    type() {
      return this.importLevels.find((level) => level.key === this.importLevel)
    },
    getDiagnosticSchemaUrl() {
      if (this.importLevel === "SIMPLE") {
        return this.diagnosticSimpleSchemaUrl
      } else if (this.importLevel === "CC_SIMPLE") {
        return this.diagnosticSimpleCCSchemaUrl
      } else if (this.importLevel === "COMPLETE") {
        return this.diagnosticCompleteSchemaUrl
      } else if (this.importLevel === "CC_COMPLETE") {
        return this.diagnosticCompleteSchemaUrl
      }
      return ""
    },
    downloadLinks() {
      const labels = {
        csv: "CSV",
      }
      const importSizes = {
        CC_COMPLETE: {
          csv: "5.5 ko",
        },
        CC_SIMPLE: {
          csv: "782 o",
        },
        COMPLETE: {
          csv: "5 Ko",
        },
        SIMPLE: {
          csv: "771 o",
        },
      }
      let filename = "/static/documents/"
      if (this.importLevel === "COMPLETE") filename = filename + "fichier_exemple_complet_ma_cantine"
      else if (this.importLevel === "CC_SIMPLE") filename = filename + "fichier_exemple_ma_cantine_cc_simple"
      else if (this.importLevel === "CC_COMPLETE") filename = filename + "fichier_exemple_ma_cantine_cc_complet"
      else filename = filename + "fichier_exemple_ma_cantine"
      return ["csv"].map((fileType) => ({
        href: `${filename}.${fileType}`,
        label: `Télécharger le fichier exemple en format ${labels[fileType]}`,
        sizeStr: importSizes[this.importLevel][fileType],
      }))
    },
    importDocString() {
      return {
        SIMPLE: "l'import simple",
        COMPLETE: "l'import complet",
        CC_SIMPLE: "la mise à jour des restaurants satellites et l'import simple",
        CC_COMPLETE: "la mise à jour des restaurants satellites et l'import complet",
      }[this.importLevel]
    },
    staffImportAvailable() {
      return this.importLevel === "SIMPLE"
    },
  },
  created() {
    document.title = `${this.type.title} - Importer des bilans - ${this.$store.state.pageTitleSuffix}`
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
          this.encodingUsed = json.encoding
          let resultMessage = {
            message:
              this.canteenCount > 1 ? `${this.canteenCount} cantines traitées` : `${this.canteenCount} cantine traitée`,
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
