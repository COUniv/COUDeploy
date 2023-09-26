<template>
  <div class = "CreateWrapper">
    <div class ="upload-contents">
      <el-form ref="form" :model="formCodeReview" :rules="rules" label-position="top" label-width="70px">
        <div class="category">
          <div class="selectform" style="width: 30%; margin-right: auto;">
            <Select v-model="formCodeReview.languagetype" aria-placeholder="언어" clearable size="large">
              <Option v-for="type in typeList" :value="type.value" :key="type.value">
                {{ type.label }}
              </Option>
            </Select>
          </div>

          <div style="padding-top: 15px; width: 30%; margin-left: auto; margin-top: 2px">
              <el-form-item prop="problemid" required>
                <Input v-model="formCodeReview.problemid" :border="true" placeholder="문제 번호" size="large"></Input>
              </el-form-item>
          </div>
        </div>

        <div class="title_form">
          <el-form-item prop="title" required>
            <!-- 게시글 제목 입력 - formArticle.title -->
            <el-input v-model="formCodeReview.title" :border="true" placeholder="제목" size="large"></el-input>
          </el-form-item>
        </div>

        <div class="contents_form">
          <el-form-item prop="content" required>
            <Simditor v-model="formCodeReview.content">
            </Simditor>
          </el-form-item>
        </div>

        <div class="code_form">
          <p class="caTitle">코드 작성</p>
          <el-form-item prop="code" required>
            <textarea v-model="formCodeReview.code" class="codeArea" placeholder="코드 입력해주세요" style="width: 100%; height: 300px; padding-left: 20px; padding-top: 10px"></textarea>
          </el-form-item>
        </div>

        <div class="submit_btn">
          <Button type="primary" size="large" @click="submit">제출 <Icon id="submit-icon" size="17" type="ios-paper-plane"/> </Button>
          <Button class = "cancelBtn" size="large" onclick="history.back()">취소</Button>
        </div>

      </el-form>
    </div>
  </div>
</template>

<script>
  import Simditor from '@/pages/admin/components/Simditor'
  import api from '@oj/api'
  export default {
    name: 'CreateReviewCode',
    components: {
      Simditor
    },
    data () {
      return {
        typeList: [
          {
            value: '1',
            label: 'C++'
          },
          {
            value: '2',
            label: 'C'
          },
          {
            value: '3',
            label: 'Kotlin'
          },
          {
            value: '4',
            label: 'Python'
          },
          {
            value: '5',
            label: 'Java'
          }
        ],
        rules: {
          title: [{ required: true, message: '제목은 6이상 30이하 자리까지만 허용됩니다.', trigger: 'blur', min: 6, max: 30 }],
          content: [{ required: true, message: 'Content is required', trigger: 'blur' }]
        },
        formCodeReview: { 
          title: '', 
          content: '', 
          languagetype: '', 
          problemid: '', 
          code: []
        }
      }
    },
    computed: {
      processedCode () {
        return this.formCodeReview.code.split('\n')
      }
    },
    methods: {
      submit () {
  const data = {
    title: this.formCodeReview.title,
    content: this.formCodeReview.content,
    code: this.formCodeReview.code.join('\n') // 배열을 문자열로 변환
  }
  api.CreateReviewCode(data).then(res => {
    this.$success('success!!')
    this.$router.push({name: 'codereviewmain'}).catch(() => {})
  }).catch(err => {
    // API 호출이 실패했을 때의 에러 핸들링
    console.error(err);
    this.$message.error('게시글 작성 중 오류가 발생했습니다.');
  });
}

    }
  }
</script>

<style scoped lang="less">
  .CreateWrapper {
    width : 100%;
    height : 100%;
    margin : 0; 
    padding : 0;
  }
  .upload-contents {
    width : 100%;
    height : 100%;
    display : flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  .category {
    width : 100%;
    display : flex;
    align-items: center;
  }
  .caTitle {
    font-size: 1.5rem;
    margin : 0 0 20px 5px;
    font-weight: bold;
  }
  .cancelBtn {
    margin-left: 20px;
  }
  .codeArea {
    font-size : 15px;
    border : 1px solid rgb(219, 219, 219);
    border-radius: 7px;
  }
  .codeArea textarea::placeholder {
    color: rgb(237, 237, 237);
  }
  
</style>