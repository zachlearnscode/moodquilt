<template>
  <div v-if="initializing">Initializing...</div>
  <div v-else class="border">
    <div
      v-for="(week, weekIndex) in moods"
      :key="weekIndex"
      class="flex max-w-[750px]"
    >
        <div
          v-for="(day, dayIndex) in week"
          :key="dayIndex"
          :class="getSquareColor(day?.mood)"
          class="grow aspect-square w-full min-w-[50px] p-1"
        >
          {{ day?.mood || ''}}
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue';
import dayjs from "dayjs";

const moods = ref(null);

const initializing = ref(true);
onBeforeMount(async () => {
  try {
    const res = await fetch(import.meta.env.VITE_API_URL);
    const data = await res.json();

    moods.value = data;
    let latestWeek = moods.value[moods.value.length - 1];
    if (latestWeek.length < 7) {
      latestWeek.push(...Array(7 - latestWeek.length))
    }
  } finally {
    initializing.value = false;
  }
})

const getSquareColor = (mood) => {
  switch (mood) {
    case 1:
      return "bg-violet-500 text-violet-300"
    case 2:
      return "bg-blue-500 text-blue-300"
    case 3:
      return "bg-emerald-500 text-emerald-300"
    case 4:
      return "bg-yellow-500 text-yellow-300"
    case 5:
      return "bg-red-500 text-red-300"
    default:
      return "bg-white-500 text-white-300"
  }
}
</script>