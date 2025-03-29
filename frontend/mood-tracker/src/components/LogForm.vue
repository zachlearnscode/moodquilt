<template>
  <form @submit.prevent="onSubmit">
    <template
      v-for="mood in form.mood.options"
      :key="mood.value"
    >
      <div style="display: flex; gap: 10px;">
        <input
          v-model="form.mood.selected"
          :value="mood"
          :id="mood.label.replaceAll(' ', '_')"
          type="radio"
        />
        <label
          :for="mood.label.replaceAll(' ', '_')"
          style="display: flex; align-items: center; gap: 5px;"
        >
          <div :style="`height: 1rem; aspect-ratio: 1/1;background-color: ${mood.hexCode};`"></div>
          {{ mood.label }}
        </label>
      </div>
    </template>

    <div>
      <label for="note">Note (optional)</label>
      <textarea
        v-model="form.note"
        name="note"
        id="note"
      />
    </div>

    <button type="submit">Submit</button>
  </form>
</template>

<script setup>
import { reactive, onBeforeMount } from "vue";

onBeforeMount(() => form.mood.selected = form.mood.options[2])

const form = reactive({
  mood: {
    selected: null,
    options: [
      {
        label: 'Very Unpleasant',
        value: 1,
        hexCode: "#848C8E"
      }, 
      {
        label: 'Slightly Unpleasant',
        value: 2,
        hexCode: "#435058"
      },
      {
        label: 'Neutral',
        value: 3,
        hexCode: "#DCF763"
      },
      {
        label: 'Slightly Pleasant',
        value: 4,
        hexCode: "#BFB7B6"
      },
      {
        label: 'Very Pleasant',
        value: 5,
        hexCode: "#F1F2EE"
      }
    ]
  },
  note: ''
});

const onSubmit = async () => {
  try {
    const body = {
      user_id: 3,
      mood: form.mood.selected.value,
      note: form.note.trim() || null
    }

    await fetch(`${import.meta.env.VITE_API_URL}/log-mood`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
  } catch (err) {
    console.error(err);
  }
}
</script>