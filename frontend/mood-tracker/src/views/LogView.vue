<template>
  <LogForm />
</template>

<script setup>
  import { reactive, ref } from 'vue';
  import { useRouter } from "vue-router";

  import LogForm from "../components/LogForm.vue";

  const router = useRouter();
  
  const mood = ref('Neutral');
  const moods = reactive({
    'Very unpleasant': '#848C8E',
    'Slightly unpleasant': '#435058',
    'Neutral': '#DCF763',
    'Slightly pleasant': '#BFB7B6',
    'Very pleasant': '#F1F2EE'
  });

  const onSubmit = () => {
    router.push('/')
  }
</script>

<style scoped>
  .flex {
    display: flex;
  }
  .wrapper {
    flex-direction: column;
    gap: 1rem;
  }

  .options {
    align-items: center;
    justify-content: space-between;
  }

  .mood {
    aspect-ratio: 1/1;
    border: 1px solid black;
  }
</style>