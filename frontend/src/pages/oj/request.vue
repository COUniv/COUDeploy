<template>
  <div class="custom-file">
    <form>
      <input type="file" @change="handleFileChange($event)">
      <button @click="submitForm($event)">전송</button>
    </form>
  </div>
</template>

<script>
  // 사진요청
  export default {
    data () {
      return {
        file: '',
        message: 'Hello, world'
      }
    },
    methods: {
      handleFileChange (e) {
        this.file = e.target.files[0]
        console.log(this.file)
      },
      submitForm (event) {
        event.preventDefault()
          /* global FormData */
        let formData = new FormData()
        formData.append('name', this.name)
        formData.append('age', this.age)
        formData.append('file', this.file)

        let config = {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
        this.$http.post('/admin/input_banner', formData, config).then(function (res) {
          if (res.status === 2000) {
            /*     */
          }
        })
      }
    }
  }
</script>
