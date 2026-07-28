<script setup>
import { computed } from "vue"
import { useRouter } from "vue-router"
import { computedAsync } from "@vueuse/core"
import { useRootStore } from "@/stores/root"
import managersService from "@/services/managers.js"

const props = defineProps(["canteenId"])
const emit = defineEmits(["delete"])
const store = useRootStore()
const router = useRouter()
const loggedUserEmail = computed(() => store.loggedUser?.email)

/* Managers */
const managers = computedAsync(async () => await managersService.fetchManagers(props.canteenId), [])
const managerInvitations = computedAsync(async () => await managersService.fetchManagerInvitations(props.canteenId), [])

/* Table */
const tableHeaders = [
  { key: "name", label: "Nom" },
  { key: "email", label: "E-mail" },
  { key: "status", label: "Statut" },
  { key: "actions", label: "Action" },
]

const teamRows = computed(() => {
  const managerRows = managers.value.map((manager) => ({
    ...manager,
    isMe: manager.email === loggedUserEmail.value,
    isInvitation: false,
  }))

  const invitationRows = managerInvitations.value.map((invitation) => ({
    ...invitation,
    firstName: invitation.firstName || "",
    lastName: invitation.lastName || "",
    isStaff: false,
    isInvitation: true,
  }))

  return [...invitationRows, ...managerRows]
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
  if (member.isStaff) return { label: "Administrateur ma cantine", type: "info" }
  if (member.isInvitation) return { label: "Invitation envoyée", type: "new" }
  return { label: "Gestionnaire", type: "success" }
}

const getActions = (member) => {
  if (member.isMe) return { type: "edit" }
  if (member.isStaff) return { type: "none" }
  return { type: "delete", member }
}

/* Pagination */
const minPagination = 10
const showPagination = computed(() => teamRows.value.length > minPagination)

/* Edit account */
const goToAccount = () => {
  router.push({ name: "AccountSummaryPage" })
}
</script>

<template>
  <LayoutTable>
    <DsfrDataTable
      title="Gestionnaires de l'établissement"
      no-caption
      :headers-row="tableHeaders"
      :rows="tableRows"
      :pagination="showPagination"
      :pagination-options="[minPagination, 20, 30]"
      :rows-per-page="minPagination"
      pagination-wrapper-class="fr-mt-4w"
    >
      <template #cell="{ colKey, cell }">
        <template v-if="colKey === 'name'">
          {{ cell }}
        </template>
        <template v-else-if="colKey === 'email'">
          {{ cell }}
        </template>
        <template v-else-if="colKey === 'status'">
          <DsfrBadge small :label="cell.label" :type="cell.type" />
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
  </LayoutTable>
</template>
