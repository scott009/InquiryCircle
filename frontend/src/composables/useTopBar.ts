import { ref } from 'vue'

const circleName = ref('')
const userName = ref('User')

export function useTopBar() {
  const setCircleName = (name: string) => {
    circleName.value = name
  }

  const setUserName = (name: string) => {
    userName.value = name
  }

  const clearCircleName = () => {
    circleName.value = ''
  }

  return {
    circleName,
    userName,
    setCircleName,
    setUserName,
    clearCircleName
  }
}
