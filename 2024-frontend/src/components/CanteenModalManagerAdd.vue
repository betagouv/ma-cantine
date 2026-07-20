<script setup>
import { ref, reactive, computed } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { useValidators } from "@/validators.js"
import { formatError } from "@/utils.js"
import { useRootStore } from "@/stores/root"
import managersService from "@/services/managers.js"

const props = defineProps(["opened", "canteen"])
const emit = defineEmits(["close", "updated"])
const store = useRootStore()
const loading = ref(false)

/* Canteen informations */
const canteenId = computed(() => props.canteen.id)
const canteenName = computed(() => props.canteen.name)

/* Validation */
const form = reactive({email: ""})
const { required, email } = useValidators()
const rules = {
  email: { required, email },
}
const v$ = useVuelidate(rules, form)

/* Actions */
const closeModal = () => {
  form.email = ""
  v$.value.$reset()
  loading.value = false
  emit("close")
 }
const submit = async () => {
  const isValid = await v$.value.$validate()
  if (!isValid) return
  loading.value = true
  const emailValue = form.email.trim()
  managersService
    .addManager(canteenId.value, emailValue)
    .then((response) => {
      if (response.status === "error" || response instanceof Error) {
        store.notifyServerError(response)
      } else {
        store.notify({
          title: "Mise à jour prise en compte",
          message: `${emailValue} a bien été ajouté aux gestionnaires de cet établissement.`,
          status: "success",
        })
        emit("updated", response)
        emit("close")
      }
      loading.value = false
    })
    .catch((e) => {
      loading.value = false
      store.notifyServerError(e)
    })
}
</script>

<template>
  <DsfrModal
    :opened="opened"
    :title="`Ajouter un gestionnaire à « ${canteenName} »`"
    @close="closeModal"
    :actions="[
      {
        label: 'Ajouter',
        disabled: loading,
        onClick() {
          submit()
        },
      },
      {
        label: 'Annuler',
        secondary: true,
        onClick() {
          closeModal()
        },
      },
    ]"
  >
    <p>
      Pour ajouter un gestionnaire à cet établissement il vous suffit de renseignez son adresse e-mail.
    </p>
    <p>
      Si l'adresse mail existe sur <em>ma cantine</em>, il sera automatiquement ajouté, si non une invitation pour créer son compte lui sera envoyée par e-mail.
    </p>
    <DsfrInputGroup
      v-model="form.email"
      label="Adresse e-mail"
      :label-visible="true"
      type="email"
      :error-message="formatError(v$.email)"
      @keydown.enter.prevent="submit"
      :disabled="loading"
    />
  </DsfrModal>
</template>
