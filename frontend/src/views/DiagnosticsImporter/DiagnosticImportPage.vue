<template>
  <div class="text-left">
    <BreadcrumbsNav
      :links="[{ to: { name: 'ManagementPage' } }, { to: { name: 'DiagnosticsImporter' } }]"
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
    <v-simple-table class="my-6">
      <template v-slot:default>
        <thead>
          <tr>
            <th>Titre</th>
            <th>Champ</th>
            <th>Description</th>
            <th>Type</th>
            <th>Exemple</th>
            <th>Obligatoire</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(field, idx) in sharedDocumentation" :key="idx">
            <td>{{ field.title }}</td>
            <td>{{ field.name }}</td>
            <td v-html="field.description"></td>
            <td>{{ field.type }}</td>
            <td style="min-width: 160px;">{{ field.example }}</td>
            <td class="text-center">{{ field.optional ? "✘" : "✔" }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
    <p v-if="ccDocumentation && ccDocumentation.length > 0">
      Les champs suivants concernent les livreurs des repas
    </p>
    <v-simple-table class="mt-0 mb-6" v-if="ccDocumentation.length && ccDocumentation.length > 0">
      <template v-slot:default>
        <thead>
          <tr>
            <th>Titre</th>
            <th>Champ</th>
            <th>Description</th>
            <th>Type</th>
            <th>Exemple</th>
            <th>Obligatoire</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(field, idx) in ccDocumentation" :key="idx">
            <td>{{ field.title }}</td>
            <td>{{ field.name }}</td>
            <td v-html="field.description"></td>
            <td>{{ field.type }}</td>
            <td>{{ field.example }}</td>
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
            <th>Titre</th>
            <th>Champ</th>
            <th>Description</th>
            <th>Type</th>
            <th>Exemple</th>
            <th>Obligatoire</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(field, idx) in diagnosticDocumentation" :key="idx">
            <td>{{ field.title }}</td>
            <td>{{ field.name }}</td>
            <td v-html="field.description"></td>
            <td>{{ field.type }}</td>
            <td>{{ field.example }}</td>
            <td class="text-center">{{ field.optional ? "✘" : "✔" }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
    <p v-else>Aucune autre colonne requise.</p>

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

export default {
  name: "DiagnosticImportPage",
  components: { BreadcrumbsNav, FileDrop, HelpForm, DownloadLinkList, DsfrCallout, ImporterSuccessDialog },
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
      sharedDocumentation: [
        {
          title: "siret",
          name: "SIRET de l'établissement",
          description: "Ce SIRET doit être unique car il correspond à un lieu physique.",
          type: "14 chiffres, avec ou sans espaces",
          example: "000 000 000 00000",
        },
        {
          title: "nom",
          name: "Nom de l'établissement",
          example: "Ma Cantine",
          type: "Texte libre",
        },
        {
          title: "code_insee_commune",
          name: "Code géographique INSEE de la ville",
          example: "69123",
          optional: true,
        },
        {
          title: "code_postal_commune",
          name: "Code postal",
          description: "En cas d'absence de code INSEE, ce champ devient obligatoire.",
          example: "69001",
          optional: true,
        },
        {
          title: "siret_livreur_repas",
          name: "SIRET du livreur des repas",
          description:
            "Ce SIRET peut être vide ou utilisé pour plusieurs lignes, dans le cas où c'est le gestionnaire du livreur des repas qui remplit les lignes pour chaque cantine satellite.",
          type: "14 chiffres, avec ou sans espaces",
          example: "999 999 999 99999",
          optional: true,
        },
        {
          title: "nombre_repas_jour",
          name: "Nombre de repas servis par jour",
          type: "Chiffre",
          example: "300",
        },
        {
          title: "nombre_repas_an",
          name: "Nombre total de couverts à l'année",
          type: "Chiffre",
          description: "Y compris les couverts livrés",
          example: "67000",
        },
        {
          title: "secteurs",
          name: "Secteurs",
          description: `Options acceptées : ${this.$store.state.sectors.map(
            (x) => " <code>" + x.name + "</code>"
          )}. Spécifiez plusieurs en séparant avec un <code>+</code>.`,
          type: "Texte",
          example: `${this.$store.state.sectors[0].name}+${this.$store.state.sectors[1].name}`,
        },
        {
          title: "type_production",
          name: "Mode de production",
          description:
            "Le mode de production de votre cantine. Les options :<br />- <code>central</code> si vous êtes un livreur des repas sans lieu de consommation<br/>- <code>central_serving</code> si vous êtes un livreur des repas qui accueille aussi des convives sur place,<br/>- <code>site</code> si vous êtes une cantine qui produit les repas sur place, et<br/>- <code>site_cooked_elsewhere</code> si vous êtes une cantine qui sert des repas preparés par un autre établissement.<br/>",
          type: "Texte (choix unique)",
          example: "central",
        },
        {
          title: "type_gestion",
          name: "Mode de gestion",
          description:
            "Comment le service des repas est géré. Options acceptées : <code>direct</code> (directe) et <code>conceded</code> (concédé).",
          type: "Texte (choix unique)",
          example: "direct",
        },
        {
          title: "modèle_économique",
          name: "Secteur économique",
          description:
            "Le type d'établissement. Options acceptées : <code>public</code> et <code>private</code> (privé).",
          type: "Texte (choix unique)",
          example: "public",
          optional: true,
        },
        {
          title: "gestionnaires_additionnels",
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
    ccDocumentation() {
      if (this.importLevel !== "CC_SIMPLE" && this.importLevel !== "CC_COMPLETE") return []
      return [
        {
          title: "satellite_canteens_count",
          name: "Nombre de cantines satellites",
          description:
            "Nombre de cantines/lieux de service à qui je fournis des repas. Obligatoire pour les livreurs des repas.",
          type: "Chiffre entier",
          example: "14",
          optional: true,
        },
      ]
    },
    diagnosticDocumentation() {
      if (this.importLevel === "NONE") return []
      const numberFormatExample = "En format <code>1234</code>/<code>1234.5</code>/<code>1234.56</code>."
      const simpleValues = [
        { title: "valeur_bio", name: "Valeur d'achats bio HT" },
        { title: "valeur_siqo", name: "Valeur d'achats SIQO (hors bio) HT" },
        {
          title: "valeur_environnemental",
          name:
            "Valeur (en € HT) de mes achats prenant en compte les coûts imputés aux externalités environnementales ou acquis sur la base de leurs performances en matière environnementale",
        },
        { title: "valeur_autres_egalim", name: "Valeur (en € HT) des autres achats EGAlim" },
        {
          title: "valeur_viandes",
          name: "Valeur (en € HT) de mes achats en viandes et volailles fraiches ou surgelées total",
        },
        {
          title: "valeur_viandes_egalim",
          name: "Valeur (en € HT) de mes achats EGAlim en viandes et volailles fraiches ou surgelées",
        },
        {
          title: "valeur_viandes_france",
          name: "Valeur (en € HT) de mes achats provenance France en viandes et volailles fraiches ou surgelées",
        },
        {
          title: "valeur_poissons",
          name: "Valeur (en € HT) de mes achats en poissons, produits de la mer et de l'aquaculture total",
        },
        {
          title: "valeur_poissons_egalim",
          name: "Valeur (en € HT) de mes achats EGAlim en poissons, produits de la mer et de l'aquaculture",
        },
      ]
      let valuesArray = simpleValues
      const array = [
        {
          title: "année_bilan",
          name: "Année du bilan",
          description: "En format <code>YYYY</code>.",
          type: "Chiffre",
          example: "2020",
        },
        {
          title: "valeur_totale",
          name: "Valeur totale d'achats HT",
          description: numberFormatExample,
          type: "Chiffre",
          example: "1234.99",
        },
      ]
      if (this.importLevel === "COMPLETE" || this.importLevel === "CC_COMPLETE") {
        valuesArray = [
          {
            title: "valeur_viandes_volailles",
            name: "La valeur totale (en € HT) de mes achats en viandes et volailles fraiches ou surgelées",
          },
          {
            title: "valeur_poissons_produits_mer",
            name: "La valeur totale (en € HT) de mes achats en poissons, produits de la mer et de l'aquaculture",
          },
          { title: "valeur_bio_viandes_volailles", name: "Bio : Viandes et volailles fraîches et surgelées" },
          { title: "valeur_bio_produits_aquatiques", name: "Bio : Produits aquatiques frais et surgelés" },
          { title: "valeur_bio_fruits_legumes", name: "Bio : Fruits et légumes frais et surgelés" },
          { title: "valeur_bio_charcuterie", name: "Bio : Charcuterie" },
          { title: "valeur_bio_bof", name: "Bio : BOF (Produits laitiers, beurre et œufs)" },
          { title: "valeur_bio_boulangerie_patisserie", name: "Bio : Boulangerie/Pâtisserie fraîches" },
          { title: "valeur_bio_boissons", name: "Bio : Boissons" },
          { title: "valeur_bio_autres_produits", name: "Bio : Autres produits frais, surgelés et d’épicerie" },
          {
            title: "valeur_label_rouge_viandes_volailles",
            name: "Label rouge : Viandes et volailles fraîches et surgelées",
          },
          {
            title: "valeur_label_rouge_produits_aquatiques",
            name: "Label rouge : Produits aquatiques frais et surgelés",
          },
          { title: "valeur_label_rouge_fruits_legumes", name: "Label rouge : Fruits et légumes frais et surgelés" },
          { title: "valeur_label_rouge_charcuterie", name: "Label rouge : Charcuterie" },
          { title: "valeur_label_rouge_bof", name: "Label rouge : BOF (Produits laitiers, beurre et œufs)" },
          { title: "valeur_label_rouge_boulangerie_patisserie", name: "Label rouge : Boulangerie/Pâtisserie fraîches" },
          { title: "valeur_label_rouge_boissons", name: "Label rouge : Boissons" },
          {
            title: "valeur_label_rouge_autres_produits",
            name: "Label rouge : Autres produits frais, surgelés et d’épicerie",
          },
          {
            title: "valeur_aoc_aop_igp_stg_viandes_volailles",
            name: "AOC / AOP / IGP / STG : Viandes et volailles fraîches et surgelées",
          },
          {
            title: "valeur_aoc_aop_igp_stg_produits_aquatiques",
            name: "AOC / AOP / IGP / STG : Produits aquatiques frais et surgelés",
          },
          {
            title: "valeur_aoc_aop_igp_stg_fruits_legumes",
            name: "AOC / AOP / IGP / STG : Fruits et légumes frais et surgelés",
          },
          { title: "valeur_aoc_aop_igp_stg_charcuterie", name: "AOC / AOP / IGP / STG : Charcuterie" },
          {
            title: "valeur_aoc_aop_igp_stg_bof",
            name: "AOC / AOP / IGP / STG : BOF (Produits laitiers, beurre et œufs)",
          },
          {
            title: "valeur_aoc_aop_igp_stg_boulangerie_patisserie",
            name: "AOC / AOP / IGP / STG : Boulangerie/Pâtisserie fraîches",
          },
          { title: "valeur_aoc_aop_igp_stg_boissons", name: "AOC / AOP / IGP / STG : Boissons" },
          {
            title: "valeur_aoc_aop_igp_stg_autres_produits",
            name: "AOC / AOP / IGP / STG : Autres produits frais, surgelés et d’épicerie",
          },
          {
            title: "valeur_certification_environnementale_viandes_volailles",
            name: "Certification environnementale de niveau 2 ou HVE : Viandes et volailles fraîches et surgelées",
          },
          {
            title: "valeur_certification_environnementale_produits_aquatiques",
            name: "Certification environnementale de niveau 2 ou HVE : Produits aquatiques frais et surgelés",
          },
          {
            title: "valeur_certification_environnementale_fruits_legumes",
            name: "Certification environnementale de niveau 2 ou HVE : Fruits et légumes frais et surgelés",
          },
          {
            title: "valeur_certification_environnementale_charcuterie",
            name: "Certification environnementale de niveau 2 ou HVE : Charcuterie",
          },
          {
            title: "valeur_certification_environnementale_bof",
            name: "Certification environnementale de niveau 2 ou HVE : BOF (Produits laitiers, beurre et œufs)",
          },
          {
            title: "valeur_certification_environnementale_boulangzrie_patisserie",
            name: "Certification environnementale de niveau 2 ou HVE : Boulangerie/Pâtisserie fraîches",
          },
          {
            title: "valeur_certification_environnementale_boissons",
            name: "Certification environnementale de niveau 2 ou HVE : Boissons",
          },
          {
            title: "valeur_certification_environnementale_autres_produits",
            name: "Certification environnementale de niveau 2 ou HVE : Autres produits frais, surgelés et d’épicerie",
          },
          {
            title: "valeur_peche_durable_viandes_volailles",
            name: "Pêche durable : Viandes et volailles fraîches et surgelées",
          },
          {
            title: "valeur_peche_durable_produits_aquatiques",
            name: "Pêche durable : Produits aquatiques frais et surgelés",
          },
          { title: "valeur_peche_durable_fruits_legumes", name: "Pêche durable : Fruits et légumes frais et surgelés" },
          { title: "valeur_peche_durable_charcuterie", name: "Pêche durable : Charcuterie" },
          { title: "valeur_peche_durable_bof", name: "Pêche durable : BOF (Produits laitiers, beurre et œufs)" },
          {
            title: "valeur_peche_durable_boulangerie_patisserie",
            name: "Pêche durable : Boulangerie/Pâtisserie fraîches",
          },
          { title: "valeur_peche_durable_boissons", name: "Pêche durable : Boissons" },
          {
            title: "valeur_peche_durable_autres_produits",
            name: "Pêche durable : Autres produits frais, surgelés et d’épicerie",
          },
          {
            title: "valeur_region_ultraperipherique_viandes_volailles",
            name: "Région ultrapériphérique : Viandes et volailles fraîches et surgelées",
          },
          {
            title: "valeur_region_ultraperipherique_produits_aquatiques",
            name: "Région ultrapériphérique : Produits aquatiques frais et surgelés",
          },
          {
            title: "valeur_region_ultraperipherique_fruits_legumes",
            name: "Région ultrapériphérique : Fruits et légumes frais et surgelés",
          },
          { title: "valeur_region_ultraperipherique_charcuterie", name: "Région ultrapériphérique : Charcuterie" },
          {
            title: "valeur_region_ultraperipherique_bof",
            name: "Région ultrapériphérique : BOF (Produits laitiers, beurre et œufs)",
          },
          {
            title: "valeur_region_ultraperipherique_boulangerie_patisserie",
            name: "Région ultrapériphérique : Boulangerie/Pâtisserie fraîches",
          },
          { title: "valeur_region_ultraperipherique_boissons", name: "Région ultrapériphérique : Boissons" },
          {
            title: "valeur_region_ultraperipherique_autres_produits",
            name: "Région ultrapériphérique : Autres produits frais, surgelés et d’épicerie",
          },
          {
            title: "valeur_commerce_equitable_viandes_volailles",
            name: "Commerce équitable : Viandes et volailles fraîches et surgelées",
          },
          {
            title: "valeur_commerce_equitable_produits_aquatiques",
            name: "Commerce équitable : Produits aquatiques frais et surgelés",
          },
          {
            title: "valeur_commerce_equitable_fruits_legumes",
            name: "Commerce équitable : Fruits et légumes frais et surgelés",
          },
          { title: "valeur_commerce_equitable_charcuterie", name: "Commerce équitable : Charcuterie" },
          {
            title: "valeur_commerce_equitable_bof",
            name: "Commerce équitable : BOF (Produits laitiers, beurre et œufs)",
          },
          {
            title: "valeur_commerce_equitable_boulangerie_patisserie",
            name: "Commerce équitable : Boulangerie/Pâtisserie fraîches",
          },
          { title: "valeur_commerce_equitable_boissons", name: "Commerce équitable : Boissons" },
          {
            title: "valeur_commerce_equitable_autres_produits",
            name: "Commerce équitable : Autres produits frais, surgelés et d’épicerie",
          },
          { title: "valeur_fermier_viandes_volailles", name: "Fermier : Viandes et volailles fraîches et surgelées" },
          { title: "valeur_fermier_produits_aquatiques", name: "Fermier : Produits aquatiques frais et surgelés" },
          { title: "valeur_fermier_fruits_legumes", name: "Fermier : Fruits et légumes frais et surgelés" },
          { title: "valeur_fermier_charcuterie", name: "Fermier : Charcuterie" },
          { title: "valeur_fermier_bof", name: "Fermier : BOF (Produits laitiers, beurre et œufs)" },
          { title: "valeur_fermier_boulangerie_patisserie", name: "Fermier : Boulangerie/Pâtisserie fraîches" },
          { title: "valeur_fermier_boissons", name: "Fermier : Boissons" },
          { title: "valeur_fermier_autres_produits", name: "Fermier : Autres produits frais, surgelés et d’épicerie" },
          {
            title: "valeur_couts_externalites_viandes_volailles",
            name:
              "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie : Viandes et volailles fraîches et surgelées",
          },
          {
            title: "valeur_couts_externalites_produits_aquatiques",
            name:
              "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie : Produits aquatiques frais et surgelés",
          },
          {
            title: "valeur_couts_externalites_fruits_legumes",
            name:
              "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie : Fruits et légumes frais et surgelés",
          },
          {
            title: "valeur_couts_externalites_charcuterie",
            name:
              "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie : Charcuterie",
          },
          {
            title: "valeur_couts_externalites_bof",
            name:
              "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie : BOF (Produits laitiers, beurre et œufs)",
          },
          {
            title: "valeur_couts_externalites_boulangerie_patisserie",
            name:
              "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie : Boulangerie/Pâtisserie fraîches",
          },
          {
            title: "valeur_couts_externalites_boissons",
            name:
              "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie : Boissons",
          },
          {
            title: "valeur_couts_externalites_autres_produits",
            name:
              "Produit prenant en compte les coûts imputés aux externalités environnementales pendant son cycle de vie : Autres produits frais, surgelés et d’épicerie",
          },
          {
            title: "valeur_performances_environnementales_viandes_volailles",
            name:
              "Produits acquis sur la base de leurs performances en matière environnementale : Viandes et volailles fraîches et surgelées",
          },
          {
            title: "valeur_performances_environnementales_produits_aquatiques",
            name:
              "Produits acquis sur la base de leurs performances en matière environnementale : Produits aquatiques frais et surgelés",
          },
          {
            title: "valeur_performances_environnementales_fruits_legumes",
            name:
              "Produits acquis sur la base de leurs performances en matière environnementale : Fruits et légumes frais et surgelés",
          },
          {
            title: "valeur_performances_environnementales_charcuterie",
            name: "Produits acquis sur la base de leurs performances en matière environnementale : Charcuterie",
          },
          {
            title: "valeur_performances_environnementales_bof",
            name:
              "Produits acquis sur la base de leurs performances en matière environnementale : BOF (Produits laitiers, beurre et œufs)",
          },
          {
            title: "valeur_performances_environnementales_boulangerie_patisserie",
            name:
              "Produits acquis sur la base de leurs performances en matière environnementale : Boulangerie/Pâtisserie fraîches",
          },
          {
            title: "valeur_performances_environnementales_boissons",
            name: "Produits acquis sur la base de leurs performances en matière environnementale : Boissons",
          },
          {
            title: "valeur_performances_environnementales_autres_produits",
            name:
              "Produits acquis sur la base de leurs performances en matière environnementale : Autres produits frais, surgelés et d’épicerie",
          },
          {
            title: "valeur_non_egalim_viandes_volailles",
            name: "Non-Egalim : Viandes et volailles fraîches et surgelées",
          },
          {
            title: "valeur_non_egalim_produits_aquatiques",
            name: "Non-Egalim : Produits aquatiques frais et surgelés",
          },
          { title: "valeur_non_egalim_fruits_legumes", name: "Non-Egalim : Fruits et légumes frais et surgelés" },
          { title: "valeur_non_egalim_charcuterie", name: "Non-Egalim : Charcuterie" },
          { title: "valeur_non_egalim_bof", name: "Non-Egalim : BOF (Produits laitiers, beurre et œufs)" },
          { title: "valeur_non_egalim_boulangerie_patisserie", name: "Non-Egalim : Boulangerie/Pâtisserie fraîches" },
          { title: "valeur_non_egalim_boissons", name: "Non-Egalim : Boissons" },
          {
            title: "valeur_non_egalim_autres_produits",
            name: "Non-Egalim : Autres produits frais, surgelés et d’épicerie",
          },
          {
            title: "valeur_provenance_france_viandes_volailles",
            name: "Provenance France : Viandes et volailles fraîches et surgelées",
          },
          {
            title: "valeur_provenance_france_produits_aquatiques",
            name: "Provenance France : Produits aquatiques frais et surgelés",
          },
          {
            title: "valeur_provenance_france_fruits_legumes",
            name: "Provenance France : Fruits et légumes frais et surgelés",
          },
          { title: "valeur_provenance_france_charcuterie", name: "Provenance France : Charcuterie" },
          {
            title: "valeur_provenance_france_bof",
            name: "Provenance France : BOF (Produits laitiers, beurre et œufs)",
          },
          {
            title: "valeur_provenance_france_boulangerie_patisserie",
            name: "Provenance France : Boulangerie/Pâtisserie fraîches",
          },
          { title: "valeur_provenance_france_boissons", name: "Provenance France : Boissons" },
          {
            title: "valeur_provenance_france_autres_produits",
            name: "Provenance France : Autres produits frais, surgelés et d’épicerie",
          },
          {
            title: "valeur_circuit_court_viandes_volailles",
            name: "Circuit-court : Viandes et volailles fraîches et surgelées",
          },
          {
            title: "valeur_circuit_court_produits_aquatiques",
            name: "Circuit-court : Produits aquatiques frais et surgelés",
          },
          { title: "valeur_circuit_court_fruits_legumes", name: "Circuit-court : Fruits et légumes frais et surgelés" },
          { title: "valeur_circuit_court_charcuterie", name: "Circuit-court : Charcuterie" },
          { title: "valeur_circuit_court_bof", name: "Circuit-court : BOF (Produits laitiers, beurre et œufs)" },
          {
            title: "valeur_circuit_court_boulangerie_patisserie",
            name: "Circuit-court : Boulangerie/Pâtisserie fraîches",
          },
          { title: "valeur_circuit_court_boissons", name: "Circuit-court : Boissons" },
          {
            title: "valeur_circuit_court_autres_produits",
            name: "Circuit-court : Autres produits frais, surgelés et d’épicerie",
          },
          {
            title: "valeur_produit_local_viandes_volailles",
            name: "Produit local : Viandes et volailles fraîches et surgelées",
          },
          {
            title: "valeur_produit_local_produits_aquatiques",
            name: "Produit local : Produits aquatiques frais et surgelés",
          },
          { title: "valeur_produit_local_fruits_legumes", name: "Produit local : Fruits et légumes frais et surgelés" },
          { title: "valeur_produit_local_charcuterie", name: "Produit local : Charcuterie" },
          { title: "valeur_produit_local_bof", name: "Produit local : BOF (Produits laitiers, beurre et œufs)" },
          {
            title: "valeur_produit_local_boulangerie_patisserie",
            name: "Produit local : Boulangerie/Pâtisserie fraîches",
          },
          { title: "valeur_produit_local_boissons", name: "Produit local : Boissons" },
          {
            title: "valeur_produit_local_autres_produits",
            name: "Produit local : Autres produits frais, surgelés et d’épicerie",
          },
        ]
      }
      valuesArray.forEach((value) => {
        array.push({
          title: value.title,
          name: value.name,
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
          csv: "5.5 ko",
          ods: "21 ko",
          xlsx: "9.4 ko",
        },
        CC_SIMPLE: {
          csv: "782 o",
          ods: "17.1 ko",
          xlsx: "6 ko",
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
      else if (this.importLevel === "CC_SIMPLE") filename = filename + "fichier_exemple_ma_cantine_cc_simple"
      else if (this.importLevel === "CC_COMPLETE") filename = filename + "fichier_exemple_ma_cantine_cc_complet"
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
    staffImportAvailable() {
      return this.importLevel === "SIMPLE" || this.importLevel === "NONE"
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
