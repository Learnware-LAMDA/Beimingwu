<script setup>
import { ref, onMounted, nextTick, watch, onActivated } from 'vue'
import PageLearnwareList from '@/components/Learnware/PageLearnwareList.vue'

const learnwareItems = ref([])
const page = ref(1)
const pageNum = ref(1)
const pageSize = ref(10)

const loading = ref(false)

const contentRef = ref(null)
const scrollTop = ref(0)

const showError = ref(false)
const errorMsg = ref('')
const errorTimer = ref(null)

function deleteLearnware(id) {
  fetch('/api/user/delete_learnware', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      learnware_id: id
    }),
  })
  .then((res) => {
      if (res.status === 200) {
        return res
      }
      throw new Error('Network error')
    })
    .then((res) => res.json())
    .then((res) => {
      switch (res.code) {
        case 0: {
          learnwareItems.value.splice(learnwareItems.value.findIndex((item) => item.id === id), 1)
          fetchByFilterAndPage(page.value)
          return
        }
        default: {
          throw new Error(res.msg)
        }
      }
    })
    .catch((err) => {
      console.error(err)
      loading.value = false
      showError.value = true
      errorMsg.value = err.message
      clearTimeout(errorTimer.value)
      errorTimer.value = setTimeout(() => { showError.value = false }, 3000)
    })
}

function pageChange(newPage) {
  page.value = newPage
}

function delay(ms) {
  return new Promise((res) => {
    setTimeout(res, ms)
  })
}

function fetchByFilterAndPage(page) {
  if (contentRef.value) {
    contentRef.value.scrollTop = 0
  }

  loading.value = true

  fetch('/api/user/get_learnware_list', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      page: page,
      limit: pageSize.value,
    }),
  })
  .then((res) => {
      if (res.status === 200) {
        return res
      }
      throw new Error('Network error')
    })
    .then((res) => res.json())
    .then((res) => {
      switch (res.code) {
        case 0: {
          loading.value = false
          learnwareItems.value = res.data.learnware_list.map((item) => ({
            id: item.learnware_id,
            name: item.semantic_specification.Name.Values,
            description: item.semantic_specification.Description.Values,
            dataType: item.semantic_specification.Data.Values,
            taskType: item.semantic_specification.Task.Values,
            hardwareType: item.semantic_specification.Device.Values[0],
            Scenario: item.semantic_specification.Values
          }))
          pageNum.value = res.data.total_pages
          return
        }
        default: {
          throw new Error(res.msg)
        }
      }
    })
    .catch((err) => {
      console.error(err)
      loading.value = false
      showError.value = true
      errorMsg.value = err.message
      clearTimeout(errorTimer.value)
      errorTimer.value = setTimeout(() => { showError.value = false }, 3000)
    })
}

watch(
  () => page.value,
  (newPage) => {
    fetchByFilterAndPage(newPage)
  },
  { deep: true }
)

onActivated(() => {
  contentRef.value.scrollTop = scrollTop.value
})

onMounted(() => {
  nextTick(() => {
    contentRef.value.addEventListener('scroll', () => {
      scrollTop.value = contentRef.value.scrollTop
    })
  })

  fetchByFilterAndPage(page.value)
})
</script>

<template>
  <div ref="contentRef" class="fixed flex flex-col w-1/1 overflow-y-scroll justify-start items-center">
    <v-scroll-y-transition>
      <v-card-actions v-if="showError">
        <v-alert closable :text="errorMsg" type="error" @click:close="showError = false" />
      </v-card-actions>
    </v-scroll-y-transition>
    <div class="w-1/1 max-w-900px">
      <page-learnware-list :show-pagination="true" :items="learnwareItems" @page-change="pageChange" :page="page"
        :page-num="pageNum" :page-size="pageSize" :loading="loading" @delete="(id) => deleteLearnware(id)" :cols="1"
        :show-actions="true" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.fixed {
  height: calc(100% - var(--v-layout-top));
}
</style>