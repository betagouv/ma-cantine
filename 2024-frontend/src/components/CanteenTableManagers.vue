<script setup>
import { ref, computed, watch } from "vue"
import { useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"

const props = defineProps(["canteenInformation"])
const emit = defineEmits(["delete"])

const store = useRootStore()
const router = useRouter()
const loggedUserEmail = computed(() => store.loggedUser?.email)

const managers = ref([])
const managerInvitations = ref([])

/* Update table */
const update = (managementTeam) => {
  managers.value = managementTeam.managers || []
  managerInvitations.value = managementTeam.managerInvitations || []
}

watch(
  () => props.canteenInformation,
  (canteen) => {
    if (!canteen?.id) return
    update(canteen)
  },
  { immediate: true }
)

defineExpose({ update })

/* Table */
const tableHeaders = [
  { key: "name", label: "Nom" },
  { key: "email", label: "E-mail" },
  { key: "status", label: "Statut" },
  { key: "actions", label: "Action" },
]

const teamRows = computed(() => {
  const managerRows = (managers.value || []).map((manager) => ({
    ...manager,
    isInvitation: false,
  }))
  const invitationRows = (managerInvitations.value || []).map((invitation) => ({
    ...invitation,
    firstName: invitation.firstName || "",
    lastName: invitation.lastName || "",
    isStaff: false,
    isInvitation: true,
  }))

  const meEmail = loggedUserEmail.value
  return [...managerRows, ...invitationRows].sort((a, b) => {
    if (a.email === meEmail) return -1
    if (b.email === meEmail) return 1
    return (a.email || "").localeCompare(b.email || "", "fr", { sensitivity: "base" })
  })
})

const tableRows = computed(() =>
  teamRows.value.map((member) => ({
    name: getDisplayName(member),
    email: member.email,
    status: getStatusBadge(member),
    actions: getActions(member),
  }))
)

/* Get content */
const getDisplayName = (member) => {
  const firstName = member.firstName || ""
  const lastName = member.lastName || ""
  return `${firstName} ${lastName}`.trim()
}

const getStatusBadge = (member) => {
  if (member.isStaff) {
    return { label: "Administrateur ma cantine", type: "info" }
  }
  if (member.isInvitation) {
    return { label: "Invitation envoyée", type: "new" }
  }
  return { label: "Gestionnaire", type: "success" }
}

const getActions = (member) => {
  if (member.email === loggedUserEmail.value) return { type: "edit" }
  if (member.isStaff) return { type: "none" }
  return { type: "delete", member }
}

/* Edit account */
const goToAccount = () => {
  router.push({ name: "AccountSummaryPage" })
}
</script>

<template>
  <DsfrDataTable
    title="Gestionnaires de l'établissement"
    no-caption
    :headers-row="tableHeaders"
    :rows="tableRows"
  >
    <template #cell="{ colKey, cell }">
      <template v-if="colKey === 'name'">
        {{ cell }}
      </template>
      <template v-else-if="colKey === 'email'">
        {{ cell }}
      </template>
      <template v-else-if="colKey === 'status'">
        <DsfrBadge small :label="cell.label" :type="cell.type" no-icon />
      </template>
      <template v-else-if="colKey === 'actions'">
        <DsfrButton
          v-if="cell.type === 'edit'"
          secondary
          size="small"
          label="Modifier"
          icon="ri-pencil-line"
          @click="goToAccount"
        />
        <DsfrButton
          v-else-if="cell.type === 'delete'"
          tertiary
          size="small"
          label="Supprimer"
          icon="fr-icon-delete-bin-line"
          @click="emit('delete', cell.member)"
        />
      </template>
    </template>
  </DsfrDataTable>
</template>
