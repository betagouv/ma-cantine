import KeyMeasureDescription from '@/components/KeyMeasureDescription'
import KeyMeasureInfoCard from '@/components/KeyMeasureInfoCard'
import KeyMeasureTitle from '@/components/KeyMeasureTitle'
import keyMeasures from '@/data/key-measures.json'
import tags from '@/data/sector-tags.json'

export default {
  components: {
    KeyMeasureDescription,
    KeyMeasureInfoCard,
    KeyMeasureTitle,
  },
  data() {
    return {
      keyMeasures,
      tags
    };
  }
}
