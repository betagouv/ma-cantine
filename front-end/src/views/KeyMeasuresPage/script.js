import InfoCard from '@/views/KeyMeasuresPage/InfoCard'
import FilterButton from '@/views/KeyMeasuresPage/FilterButton'
import keyMeasures from '@/data/key-measures.json'
import tags from '@/data/sector-tags.json'

const allSectorsId = 'allSectors';

export default {
  components: {
    InfoCard,
    FilterButton
  },
  data() {
    return {
      keyMeasures,
      tags,
      activeTags: [allSectorsId],
      allSectorsId
    };
  },
  computed: {
    measuresFilteredBySector() {
      const activeTags = this.activeTags;
      function hasActiveTag(measure) {
        return (measure.tags || []).some((tag) => activeTags.includes(tag));
      }
      const hasNoTagsOrSomeActiveTag = (measure) => !measure.tags || hasActiveTag(measure);
      if(activeTags.includes(allSectorsId)) {
        return this.keyMeasures;
      } else {
        const keyMeasuresDeepCopy = JSON.parse(JSON.stringify(this.keyMeasures));
        return keyMeasuresDeepCopy.filter((measure) => {
          return hasActiveTag(measure) || (measure.subMeasures || []).some(hasActiveTag);
        }).map((measure) => {
          if(measure.subMeasures) {
            measure.subMeasures = measure.subMeasures.filter(hasNoTagsOrSomeActiveTag)
          }
          return measure;
        });
      }
    }
  },
  methods: {
    updateSectorFilter(id) {
      const tagIndex = this.activeTags.indexOf(id);
      if(tagIndex > -1) { // currently active, want to deactivate
        this.activeTags.splice(tagIndex, 1);
        // add back all to avoid losing all text on screen
        if(this.activeTags.length === 0) {
          this.activeTags.push(allSectorsId);
        }
      } else if(id === allSectorsId) {
        // reset to avoid having 'all' and other tags
        this.activeTags = [allSectorsId];
      } else {
        this.activeTags.push(id);
        // remove 'all' to avoid having 'all' and other tags
        if(this.activeTags.includes(allSectorsId)) {
          this.activeTags.splice(this.activeTags.indexOf(allSectorsId), 1);
        }
      }
    }
  }
}