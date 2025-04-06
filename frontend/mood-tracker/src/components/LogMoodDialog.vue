<template>
  <TransitionRoot appear as="template">
    <Dialog as="div" @close="onClose" class="relative z-10">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
        @before-enter="onBeforeEnter"
      >
        <div class="fixed inset-0 bg-black/25" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-center">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel class="w-full max-w-md transform overflow-hidden rounded-md bg-white p-6 text-left align-middle shadow-xl transition-all">
              <DialogTitle
                as="h3"
                class="text-lg font-medium leading-6 text-gray-900"
              >
                Log Mood for {{ dayjs(date).format('MM/DD') }}
              </DialogTitle>
              <div class="mt-2">
                <form
                  id="log-mood-form"
                  class="space-y-3"
                  @submit.prevent="onSubmit"
                >
                  <RadioGroup v-model="form.mood.selected">
                    <RadioGroupLabel>Mood</RadioGroupLabel>
                    <div class="space-y-2 mt-2">
                      <RadioGroupOption
                        v-for="option in form.mood.options"
                        :key="option.value"
                        :value="option"
                        v-slot="{ active, checked }"
                      >
                        <div
                        :class="[
                          active ? 'ring-2 ring-white/60 ring-offset-2 ring-offset-sky-300' : '',
                          checked ? 'bg-sky-900/75 text-white ' : 'bg-white '
                        ]"
                        class="relative flex cursor-pointer rounded-lg px-5 py-4 shadow-md focus:outline-none"
                        >
                          <RadioGroupLabel>
                            {{ option.label }}
                          </RadioGroupLabel>
                        </div>
                      </RadioGroupOption>
                    </div>
                  </RadioGroup>
                  <label
                    for="notes"
                    class="block mb-2 text-gray-900 dark:text-white"
                  >
                    Notes
                  </label>
                  <textarea
                    v-model="form.notes"
                    id="notes"
                    rows="4"
                    class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  />
                </form>
              </div>

              <div class="mt-4">
                <button
                  type="submit"
                  form="log-mood-form"
                  class="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                >
                  Save log
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
  import { reactive } from "vue";
  import {
    TransitionChild,
    TransitionRoot,
    Dialog,
    DialogPanel,
    DialogTitle,
    RadioGroup,
    RadioGroupLabel,
    RadioGroupOption,
  } from '@headlessui/vue';
  import dayjs from "dayjs";

  const props = defineProps({
    date: {
      type: String,
      required: true
    }
  })

  const emit = defineEmits(['close']);

  const onBeforeEnter = () => {
    form.mood.selected = form.mood.options[2];
    form.notes = '';
  }

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
    notes: ''
  });

  const onSubmit = async () => {
    const mood = form.mood.selected.value;
    const notes = form.notes;
    const date = props.date;

    try {
      await fetch(`${import.meta.env.VITE_API_URL}/log`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: 2,
          created_at_date: dayjs(date).toISOString(),
          mood: mood,
          note: notes
        })
      })
    } catch (err) {
      console.error(err)
    }
  }
</script>