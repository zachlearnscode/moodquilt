<template>
  <div class="w-full max-w-[750px]" ref="container">
    <div v-if="initializing">Initializing...</div>
    <div
      v-else
      v-for="(week, weekIndex) in moods"
      :key="weekIndex"
      class="flex"
    >
        <div
          v-for="(day, dayIndex) in week"
          :key="dayIndex"
          :class="getSquareColor(day?.mood)"
          class="grow aspect-square w-full min-w-[50px] p-1"
        >
          {{ day?.mood || '' }}
          <br>
          {{ day?.created_at_date || '' }}
        </div>
    </div>
  </div>
  <template v-if="isTodayEditable">
    <button
      type="button"
      class="fixed bottom-0 mb-17 bg-amber-300 p-3 rounded-full hover:bg-amber-400 shadow-xl"
      @click="isOpen = true"
    >
      Log Today's Mood
    </button>
    <LogMoodDialog
      :show="isOpen"
      @close="isOpen = false"
    />
  </template>
</template>

<script setup>
import { ref, onBeforeMount, useTemplateRef, nextTick } from 'vue';
import LogMoodDialog from '@/components/LogMoodDialog.vue';
import dayjs from "dayjs";

const emit = defineEmits(["scroll-to-bottom"])

const moods = ref(null);
const isTodayEditable = ref(null);
const container = useTemplateRef('container');
const isOpen = ref(false);

const initializing = ref(true);
onBeforeMount(async () => {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/moods`);
    const data = await res.json();

    moods.value = data;
    let latestWeek = moods.value[moods.value.length - 1];
  
    isTodayEditable.value = latestWeek[latestWeek.length - 1].mood == 0;
    if (latestWeek.length < 7) latestWeek.push(...Array(7 - latestWeek.length));
  } finally {
    initializing.value = false;
    await nextTick();
    container.value.scrollIntoView({ behavior: 'instant', block: 'end' })
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