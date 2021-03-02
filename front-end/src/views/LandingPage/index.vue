<template>
  <PresentationBlock/>

  <KeyGoalsBlock/>

  <GoalBlock/>

  <div class="divider"></div>

  <DiscoverMeasuresBlock/>

  <NewsletterBlock/>
</template>

<script>
  import PresentationBlock from '@/views/LandingPage/PresentationBlock';
  import KeyGoalsBlock from '@/views/LandingPage/KeyGoalsBlock';
  import GoalBlock from '@/views/LandingPage/GoalBlock';
  import DiscoverMeasuresBlock from '@/views/LandingPage/DiscoverMeasuresBlock';
  import NewsletterBlock from '@/views/LandingPage/NewsletterBlock';

  export default {
    components: {
      PresentationBlock,
      KeyGoalsBlock,
      GoalBlock,
      DiscoverMeasuresBlock,
      NewsletterBlock,
    },
  }
</script>

<style scoped>
  .divider {
    height: 50px;
    background-image: url('../../assets/divider-section.png');
  }
</style>
