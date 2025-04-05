<template>
  <div v-if="initializing">Initializing...</div>
  <div
    v-else
    v-for="week in moods"
    :key="index"
    style="display: flex;"
  >
    <div
      v-for="day in week"
      :key="index"
      class="square"
      :style="{ 'background-color': getSquareColor(day) }"
    >
      {{ day.created_at_date }}
    </div>
    <template v-if="week.length < 7">
      <div
        v-for="n in 7 - week.length"
        :key="n"
        class="square"
      />
    </template>
  </div>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue';
import dayjs from "dayjs";

const moods = ref([]);

const initializing = ref(true);
onBeforeMount(async () => {
  try {
    const res = await fetch(import.meta.env.VITE_API_URL);
    const data = await res.json();

    moods.value = data;
  } finally {
    initializing.value = false;
  }
})

const getSquareColor = ({ mood }) => {
  switch (mood) {
    case 1:
      return "#848C8E"
    case 2:
      return "#435058"
    case 3:
      return "#DCF763"
    case 4:
      return "#BFB7B6"
    case 5:
      return "#F1F2EE"
    default:
      return "#FFFFFF"
  }
}
</script>

<style scoped>
.square {
  flex: 1;                      /* Flexible sizing */
  aspect-ratio: 1 / 1;           /* Maintain square shape */
  min-width: 50px;              /* Prevent squares from getting too small */
}
</style>