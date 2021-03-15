<template>
  <PresentationBlock/>

  <ActionsBlock/>

  <KeyGoalsBlock/>

  <GoalBlock/>

  <div class="divider"></div>

  <DiscoverMeasuresBlock/>
</template>

<script>
  import PresentationBlock from '@/views/LandingPage/PresentationBlock';
  import ActionsBlock from '@/views/LandingPage/ActionsBlock';
  import KeyGoalsBlock from '@/views/LandingPage/KeyGoalsBlock';
  import GoalBlock from '@/views/LandingPage/GoalBlock';
  import DiscoverMeasuresBlock from '@/views/LandingPage/DiscoverMeasuresBlock';

  export default {
    components: {
      PresentationBlock,
      ActionsBlock,
      KeyGoalsBlock,
      GoalBlock,
      DiscoverMeasuresBlock,
    },
  }
</script>

<style scoped>
  .divider {
    height: 50px;
    background-image: url('../../assets/divider-section.png');
  }
</style>
