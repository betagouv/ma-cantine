<script setup>
import { reactive } from "vue"
import { useRootStore } from "@/stores/root"
import { useVuelidate } from "@vuelidate/core"
import { useValidators } from "@/validators.js"
import { formatError } from "@/utils.js"
import { trackEvent } from "@/services/matomo.js"
import { inquiries } from "@/constants/form-send-inquiry.js"

/* Store */
const store = useRootStore()

/* Images */
const sittingDoodle = "/static/images/doodles-dsfr/primary/SittingDoodle.png"

/* Save user meta info */
const meta = {
  userId: store.loggedUser?.id,
  userAgent: navigator.userAgent,
}

/* Pre-fill fields with user infos */
let defaultEmail = ""
let defaultName = ""
let defaultUsername = ""
if (store.loggedUser) {
  const { email, firstName, lastName, username } = store.loggedUser
  defaultEmail = email
  defaultName = `${firstName} ${lastName}`
  defaultUsername = username
}

/* Form fields */
const form = reactive({})
const initFields = () => {
  form.fromEmail = defaultEmail
  form.name = defaultName
  form.username = defaultUsername
  form.inquiryType = ""
  form.message = ""
  form.siretOrSiren = ""
}
initFields()

/* Fields verification */
const { required, email } = useValidators()
const rules = {
  fromEmail: { required, email },
  inquiryType: { required },
  message: { required },
}
const v$ = useVuelidate(rules, form)
const validateForm = () => {
  v$.value.$validate()
  if (v$.value.$invalid) return
  sendInquiry()
}

/* Handle inquiry name */
const getInquiryTypeDisplay = (type) => {
  const index = inquiries.findIndex((element) => element.value === type)
  return inquiries[index].display
}

/* Send Form */
const sendInquiry = () => {
  const { fromEmail, name, username, message, inquiryType, siretOrSiren } = form
  const inquiryTypeDisplay = getInquiryTypeDisplay(inquiryType)
  const payload = {
    from: fromEmail,
    name: name,
    username: username,
    message: message,
    siretOrSiren: siretOrSiren,
    inquiryType: inquiryTypeDisplay,
    meta,
  }

  store
    .sendInquiryEmail(payload)
    .then(() => {
      store.notify({
        status: "success",
        message: "Votre message a bien été envoyé. Nous reviendrons vers vous dans les plus brefs délais.",
      })

      trackEvent({ category: "inquiry", action: "send", value: inquiryType })
      initFields()
      window.scrollTo(0, 0)
      v$.value.$reset()
    })
    .catch((e) => store.notifyServerError(e))
}
</script>

<template>
  <div>
    <div class="fr-grid-row">
      <div class="fr-col-12 fr-col-lg-8">
        <form class="fr-mb-4w" @submit.prevent="validateForm">
          <DsfrSelect
            v-model="form.inquiryType"
            label="Type de demande *"
            :label-visible="true"
            :options="inquiries"
            :error-message="formatError(v$.inquiryType)"
          />
          <div class="fr-grid-row fr-grid-row--gutters fr-mb-1w">
            <div class="fr-col-12 fr-col-lg-6">
              <DsfrInputGroup
                v-model="form.fromEmail"
                label="Adresse électronique *"
                :label-visible="true"
                :error-message="formatError(v$.fromEmail)"
              />
            </div>
            <div class="fr-col-12 fr-col-lg-6">
              <DsfrInputGroup v-model="form.name" label="Prénom et Nom" :label-visible="true" />
            </div>
            <div class="fr-col-12 fr-col-lg-6">
              <DsfrInputGroup
                v-model="form.username"
                label="Nom d'utilisateur"
                hint="Laissez le champ vide si vous n'êtes pas inscrit sur la plateforme"
                :label-visible="true"
              />
            </div>
            <div class="fr-col-12 fr-col-lg-6">
              <DsfrInputGroup
                v-model="form.siretOrSiren"
                label="SIRET de la cantine ou SIREN de rattachement"
                hint="Laissez le champ vide si la demande ne concerne pas une cantine"
                :label-visible="true"
              />
            </div>
          </div>

          <DsfrInputGroup
            v-model="form.message"
            class="app-form-send-inquiry__textarea"
            label="Message *"
            hint="Ne partagez pas d'informations sensibles (par ex. mot de passe, numéro de carte bleue, etc)"
            :label-visible="true"
            is-textarea
            rows="8"
            :error-message="formatError(v$.message)"
          />
          <DsfrButton type="submit" icon="fr-icon-send-plane-fill" label="Envoyer" />
        </form>
      </div>
      <div class="fr-col-4 fr-hidden fr-unhidden-lg">
        <img :src="sittingDoodle" class="app-form-send-inquiry__illustration" alt="" />
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.app-form-send-inquiry {
  &__illustration {
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
