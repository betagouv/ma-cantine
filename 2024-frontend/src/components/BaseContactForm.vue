<script setup>
import { reactive, inject } from 'vue'
import { useRootStore } from '@/stores/root'
import { useVuelidate } from "@vuelidate/core"
import { useValidators } from "@/validators.js"
import { formatError } from "@/utils.js"
import ContactFormSetting from "@/settings/contact-form.js"
import BaseMailto from '@/components/BaseMailto.vue'

/* Get from app */
const store = useRootStore()
const $matomo = inject('$matomo')

/* Save user meta info */
const meta = {
  userId: store.loggedUser?.id,
  userAgent: navigator.userAgent
}

/* Pre-fill fields with user infos */
let defaultEmail = ""
let defaultName = ""
if (store.loggedUser) {
  const { email, firstName, lastName } = store.loggedUser
  defaultEmail = email
  defaultName = `${firstName} ${lastName}`
}

/* Form fields */
const form = reactive({})
const initFields = () => {
  form.fromEmail = defaultEmail
  form.name =  defaultName
  form.inquiryType = ""
  form.message = ""
}
initFields()

/* Fields verification */
const { required, email } = useValidators()
const rules = {
  fromEmail: { required, email },
  inquiryType: { required },
  message: { required }
}
const v$ = useVuelidate(rules, form)
const validateForm = () => {
  v$.value.$validate()
  if (v$.value.$invalid) return
  else sendInquiry()
}

/* Send Form */
const sendInquiry = () => {
  const { fromEmail, name, message, inquiryType } = form
  const payload = {
    from: fromEmail,
    name: name,
    message: message,
    inquiryType: ContactFormSetting.inquiryTypeDisplay[inquiryType],
    meta,
  }

  store.sendInquiryEmail(payload)
    .then(() => {
      store.notify({
        status: "success",
        message: "Votre message a bien été envoyé. Nous reviendrons vers vous dans les plus brefs délais.",
      })

      if ($matomo) $matomo.push(['trackEvent', 'inquiry', 'send', inquiryType])
      initFields()
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
          <DsfrInputGroup
            v-model="form.fromEmail"
            label="Votre adresse électronique *"
            :label-visible="true"
            hint="Format attendu : nom@domaine.fr"
            :error-message="formatError(v$.fromEmail)"
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
            :error-message="formatError(v$.inquiryType)"
          />
          <DsfrInputGroup
            v-model="form.message"
            class="base-contact-form__textarea"
            label="Message *"
            hint="Ne partagez pas d'informations sensibles (par ex. mot de passe, numéro de carte bleue, etc)."
            :label-visible="true"
            is-textarea
            rows="8"
            :error-message="formatError(v$.message)"
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
