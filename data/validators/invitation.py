from common.utils import utils as utils_utils


def validate_invitation_creation_canteen_field(instance):
    """
    - clean_fields() (called by full_clean()) already checks that the creation_canteen field is a valid Canteen
    - extra validation:
        - creation_canteen must be a groupe
    """
    from data.models import Canteen  # avoid circular import

    errors = {}
    field_name = "creation_canteen"
    try:
        value = getattr(instance, field_name)
        if not value.is_groupe:
            utils_utils.add_validation_error(errors, field_name, "Le champ doit être une cantine de type 'Groupe'.")
    except Canteen.DoesNotExist:
        # already handled by clean_fields()
        pass
    return errors


def validate_invitation_invited_canteen_field(instance):
    """
    - clean_fields() (called by full_clean()) already checks that the invited_canteen field is a valid Canteen or empty
    - extra validation (for ADD_SATELLITE invitations):
        - invited_canteen must be filled
        - invited_canteen cannot be a groupe
        - if the invitation is pending (SENT):
            - invited_canteen cannot be already linked to a groupe
            - invited_canteen cannot have another pending invitation (from this groupe or another one)
    """
    from data.models import Canteen, Invitation  # avoid circular import

    errors = {}
    field_name = "invited_canteen"
    if instance.category != Invitation.Category.ADD_SATELLITE:
        return errors
    try:
        value = getattr(instance, field_name)
        if not value:
            utils_utils.add_validation_error(errors, field_name, "Le champ ne peut pas être vide.")
        elif value.is_groupe:
            utils_utils.add_validation_error(
                errors, field_name, "Le champ ne peut pas être une cantine de type 'Groupe'."
            )
        elif instance.status == Invitation.Status.SENT:
            if value.groupe_id:
                utils_utils.add_validation_error(errors, field_name, "Cette cantine est déjà rattachée à un groupe.")
            else:
                other_pending_invitations = Invitation.objects.filter(
                    category=Invitation.Category.ADD_SATELLITE,
                    status=Invitation.Status.SENT,
                    invited_canteen=value,
                )
                if instance.id:
                    other_pending_invitations = other_pending_invitations.exclude(id=instance.id)
                if other_pending_invitations.filter(creation_canteen_id=instance.creation_canteen_id).exists():
                    utils_utils.add_validation_error(
                        errors, field_name, "Cette cantine a déjà une invitation en attente de ce groupe."
                    )
                elif other_pending_invitations.exists():
                    utils_utils.add_validation_error(
                        errors, field_name, "Cette cantine a déjà une invitation en attente d'un autre groupe."
                    )
    except Canteen.DoesNotExist:
        # already handled by clean_fields()
        pass
    return errors


def validate_invitation_answer_fields(instance):
    """
    - extra validation:
        - if the invitation is pending (SENT): answer_user & answer_date must be empty
        - if the invitation is answered (ACCEPTED, DECLINED, CANCELLED): answer_date must be filled
          (answer_user can be empty: the user may have been deleted since)
    """
    from data.models import Invitation  # avoid circular import

    errors = {}
    if instance.status == Invitation.Status.SENT:
        if instance.answer_user_id:
            utils_utils.add_validation_error(
                errors, "answer_user", "Le champ doit être vide tant que l'invitation est en attente."
            )
        if instance.answer_date:
            utils_utils.add_validation_error(
                errors, "answer_date", "Le champ doit être vide tant que l'invitation est en attente."
            )
    elif not instance.answer_date:
        utils_utils.add_validation_error(
            errors, "answer_date", "Le champ doit être rempli une fois que l'invitation a reçu une réponse."
        )
    return errors
