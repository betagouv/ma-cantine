<template>
  <div>
    <h2 class="my-6" id="#contact">Vous avez besoin d'aide ?</h2>
    <p>
      Si votre fichier comptable agrégé ne ressemble pas du tout à ça, vous pouvez nous l'envoyer en remplissant les
      champs ci-dessous ou nous contacter directement à l'adresse
      <a href="mailto:contact@egalim.beta.gouv.fr">contact@egalim.beta.gouv.fr</a>
      .
    </p>
    <v-form v-model="helpFormIsValid" ref="helpForm" @submit.prevent class="my-12">
      <v-row class="mb-1">
        <v-col cols="12" md="6" class="py-0">
          <DsfrTextField v-model="fromEmail" label="Votre email" :rules="[validators.email]" validate-on-blur />
        </v-col>
        <v-col class="py-0">
          <DsfrTextField v-model="name" label="Prénom et nom" />
        </v-col>
      </v-row>
      <v-textarea v-model="message" label="Message (facultatif)" outlined></v-textarea>
      <v-file-input
        v-model="unusualFile"
        label="Fichier"
        outlined
        :rules="[validators.required, validators.maxFileSize(10485760, '10 Mo')]"
        validate-on-blur
        show-size
      />
      <v-btn x-large color="primary" @click="emailUnusualFile">
        <v-icon class="mr-2">mdi-send</v-icon>
        Envoyer
      </v-btn>
    </v-form>
  </div>
</template>

<script>
import validators from "@/validators"
import DsfrTextField from "@/components/DsfrTextField"

export default {
  name: "HelpForm",
  components: { DsfrTextField },
  data() {
    const user = this.$store.state.loggedUser
    return {
      validators,
      helpFormIsValid: true,
      fromEmail: user ? user.email : "",
      name: user ? `${user.firstName} ${user.lastName}` : "",
      message: "",
      unusualFile: null,
    }
  },
  methods: {
    emailUnusualFile() {
      this.$refs.helpForm.validate()
      if (!this.helpFormIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }
      let form = new FormData()
      form.append("file", this.unusualFile)
      form.append("name", this.name)
      form.append("email", this.fromEmail)
      form.append("message", this.message)
      fetch("/api/v1/emailDiagnosticImportFile/", {
        method: "POST",
        headers: {
          "X-CSRFToken": window.CSRF_TOKEN || "",
        },
        body: form,
      })
        .then((response) => {
          if (response.ok) {
            this.$store.dispatch("notify", {
              status: "success",
              title: "Fichier envoyé",
              message: "Merci, nous vous contacterons dans les plus brefs délais.",
            })
            this.unusualFile = null
            this.message = ""
          } else {
            this.$store.dispatch("notifyServerError", response)
          }
        })
        .catch((e) => {
          this.$store.dispatch("notifyServerError", e)
        })
    },
  },
}
</script>
