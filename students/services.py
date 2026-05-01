from django.db import transaction
from .models import MatriculeSequence
import logging

logger = logging.getLogger(__name__)

class MatriculeService:
    @staticmethod
    def generate_matricule(university, entry_year: int, program_code: str, level: str) -> str:
        """
        Atomically generates a unique matricule for a given university context
        using SELECT FOR UPDATE to strictly prevent race conditions.
        """
        pattern_config = university.matricule_pattern
        if not pattern_config:
            # Fallback if university hasn't configured a pattern
            pattern_config = {
                'format': '{prefix}-{program}-{level}-{sequence}',
                'sequence_length': 4
            }

        with transaction.atomic():
            # Atomically lock the sequence row for this specific cohort
            seq, created = MatriculeSequence.objects.select_for_update().get_or_create(
                university=university,
                year=entry_year,
                program_code=program_code,
                level=level,
                defaults={'current_sequence': 0}
            )

            # Increment the sequence
            seq.current_sequence += 1
            seq.save(update_fields=['current_sequence'])

            # Pad sequence with zeros based on configuration
            seq_length = pattern_config.get('sequence_length', 4)
            formatted_sequence = str(seq.current_sequence).zfill(seq_length)

            # Generate the final string
            matricule = pattern_config.get('format', '{prefix}-{sequence}').format(
                prefix=university.matricule_prefix,
                program=program_code,
                level=level,
                year=entry_year,
                sequence=formatted_sequence
            )

            return matricule
