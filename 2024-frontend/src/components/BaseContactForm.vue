<script setup>
/*
TODO :
- Validateur
- Envoyer le demande
- Meta : à voir si on l'ajoute dans la V1 du formulaire ou pas
*/

import { useRootStore } from '@/stores/root'
import { ref, reactive } from 'vue'
import { required } from "@vuelidate/validators"
import { useVuelidate } from "@vuelidate/core"
import BaseMailto from './BaseMailto.vue'
import ContactFormSetting from "@/settings/contact-form.js"

/* Pre-fill fields with user infos */
const store = useRootStore()
let defaultEmail = ""
let defaultName = ""
if (store.loggedUser) {
  const { email, firstName, lastName } = store.loggedUser
  defaultEmail = email
  defaultName = `${firstName} ${lastName}`
}

/* Form fields */
const form = reactive({
  fromEmail: defaultEmail,
  name: defaultName,
  inquiryType: "",
  message: "",
})

/* Fields verification */
const rules = {
  fromEmail: { required },
  inquiryType: { required },
  message: { required }
}
const v$ = useVuelidate(rules, form)


/* Send Form */
const hasSubmitted = ref(false)
const submitForm = () => {
  hasSubmitted.value = true
  if (v$.value.$invalid) console.log('NO SUBMIT')
  else console.log('SUBMIT')
}

// export default {
//   props: {
//     // meta is a JSON serialisable object containing data that could help the team help the user
//     // such as the page the user was on when they sent the message
//     meta: {
//       type: Object,
//       required: false,
//     },
//   },
//   data() {
//     return {
//       formIsValid: true,
//     }
//   },
//   computed: {
//     validators() {
//       return validators
//     },
//   },
//   methods: {
//     sendEmail() {
//       this.$refs.form.validate()
//       if (!this.formIsValid) {
//         this.$store.dispatch("notifyRequiredFieldsError")
//         return
//       }

//       let meta = this.meta || {}
//       meta.userId = this.$store.state.loggedUser?.id
//       meta.userAgent = navigator.userAgent

//       // this text is visible to the team when the inquiry is sent
//       const inquiryTypeDisplay = {
//         functionalityQuestion: "fonctionnalité",
//         bug: "bug",
//         egalim: "loi",
//         demo: "demande de démo",
//         other: "autre",
//       }

//       const payload = {
//         from: this.fromEmail,
//         name: this.name,
//         message: this.message,
//         inquiryType: inquiryTypeDisplay[this.inquiryType],
//         meta,
//       }

//       this.$store
//         .dispatch("sendInquiryEmail", payload)
//         .then(() => {
//           this.$store.dispatch("notify", {
//             status: "success",
//             message: `Votre message a bien été envoyé. Nous reviendrons vers vous dans les plus brefs délais.`,
//           })

//           if (this.$matomo) {
//             this.$matomo.trackEvent("inquiry", "send", this.inquiryType)
//           }
//           this.$refs.form.reset()
//           window.scrollTo(0, 0)
//         })
//         .catch((e) => this.$store.dispatch("notifyServerError", e))
//     },
//   },
// }
</script>

<template>
  <div>
    <div class="fr-grid-row">
      <div class="fr-col-8">
        <form class="fr-mb-4w" @submit.prevent="submitForm">
          <DsfrInputGroup
            v-model="form.fromEmail"
            label="Votre adresse électronique *"
            :label-visible="true"
            hint="Format attendu : nom@domaine.fr"
            :error-message="hasSubmitted && v$.fromEmail.$invalid ? 'Ce champs est requis' : false"
          />
          <DsfrInputGroup
            v-model="form.name"
            label="Prénom et nom"
            :label-visible="true"
          />
          <DsfrSelect
            v-model="form.inquiryType"
            label="Type de demande *"
            :label-visible="true"
            :options="ContactFormSetting.inquiryOptions"
            :error-message="hasSubmitted && v$.inquiryType.$invalid ? 'Ce champs est requis' : false"
          />
          <DsfrInputGroup
            v-model="form.message"
            class="base-contact-form__textarea"
            label="Message *"
            hint="Ne partagez pas d'informations sensibles (par ex. mot de passe, numéro de carte bleue, etc)."
            :label-visible="true"
            is-textarea
            rows="8"
            :error-message="hasSubmitted && v$.message.$invalid ? 'Ce champs est requis' : false"
          />
          <DsfrButton
            type="submit"
            icon="fr-icon-send-plane-fill"
            label="Envoyer"
          />
        </form>
        <DsfrCallout>
          <p>
            Si vous n'arrivez pas à utiliser le formulaire ci-dessus, vous pouvez nous contacter directement par email à
            l'adresse suivante:
            <BaseMailto />
          </p>
        </DsfrCallout>
      </div>
      <div class="fr-col-4 fr-hidden fr-unhidden-lg">
        <img src="/static/images/doodles-dsfr/primary/SittingDoodle.png" class="base-contact-form__illustration">
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.base-contact-form {
  &__illustration  {
    object-fit: contain;
    object-position: left center;
    transform: scaleX(-1);
    width: 100%;
  }

  &__textarea {
    resize: vertical;
    width: 100%;
  }
}
</style>
