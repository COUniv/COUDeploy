<template>
  <div class="setting-main">
    <div class="flex-container">
      <div v-if="routeName == 'comment-list'" class="section-title">댓글 단 게시글</div>
      <div v-if="routeName == 'like-list'" class="section-title">좋아요 한 게시글</div>
      <div>
        <!-- 게시글 목록 -->
        <Table stripe :disabled-hover="true" :columns="columns" :data="articles" :loading="loadingTable"></Table>
      </div>
      <div style="float:right">
        <Pagination :total="total" :page-size="limit" @on-change="changeRoute" :current.sync="page"></Pagination>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex'
  import api from '@oj/api'
  import utils from '@/utils/utils'
  import time from '@/utils/time'

  export default {
    data () {
      return {
        columns: [ // 열 속성 - 추후 추가 예정
          {
            title: '번호',
            align: 'center',
            render: (h, params) => {
              return h('span', params.row.id)
            }
          },
          {
            title: '제목',
            align: 'center',
            render: (h, params) => {
              return h('a',
                {
                  style: {
                    'display': 'inline-block',
                    'max-width': '150px'
                  },
                  on: { // 게시글 제목 클릭 시 해당 게시글 detail 뷰로 이동, 게시글 고유 ID 전송
                    click: () => {
                      this.$router.push({name: 'article-details', params: {articleID: params.row.id}})
                    }
                  }
                }, params.row.title)
            }
          },
          {
            title: '작성일',
            align: 'center',
            render: (h, params) => {
              return h('span', time.utcToLocal(params.row.create_time, 'YYYY-MM-DD HH:mm:ss'))
            }
          },
          {
            title: '작성자',
            align: 'center',
            render: (h, params) => {
              return h('a', {
                style: {
                  'display': 'inline-block',
                  'max-width': '150px'
                },
                on: { // 작성자명 클릭 시 해당 작성자의 프로필로 이동
                  click: () => {
                    this.$router.push(
                      {
                        name: 'user-home',
                        query: {username: params.row.username}
                      })
                  }
                }
              }, params.row.username)
            }
          },
          {
            title: '좋아요',
            align: 'center',
            render: (h, params) => {
              return h('span', params.row.like_count)
            }
          },
          {
            title: '댓글',
            align: 'center',
            render: (h, params) => {
              return h('span', params.row.comment_count)
            }
          }
        ],
        formFilter: { // 게시글을 불러올 때 필터 설정용 데이터
          username: ''
        },
        routeName: '',
        loadingTable: false,
        articles: [], // 게시글 목록
        total: 30,
        limit: 12, // 한 페이지에 출력할 최대 게시글 개수
        page: 1
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init () {
        this.routeName = this.$route.name
        let query = this.$route.query
        this.formFilter.username = query.username || ''
        if (this.page < 1) {
          this.page = 1
        }
        this.getArticles()
      },
      buildQuery () { // 쿼리로 설정한 필터값을 전송용 데이터로 빌드
        return {
          username: this.formFilter.username,
          page: this.page
        }
      },
      getArticles () { // 게시글 목록 가져오기
        let params = this.buildQuery() // 게시글 필터 데이터
        let offset = (this.page - 1) * this.limit
        this.loadingTable = true
        if (this.routeName === 'comment-list') {
          api.getCommentArticleList(offset, this.limit, params).then(res => { // 필터값을 전송하여 게시글 데이터 가져옴
            let data = res.data.data
            for (let v of data.results) {
              v.loading = false
            }
            this.loadingTable = false
            this.articles = data.results // 필터를 거쳐 나온 게시글 데이터
            this.total = data.total
          }).catch(() => {
            this.loadingTable = false
          })
        } else if (this.routeName === 'like-list') {
          api.getLikeArticleList(offset, this.limit, params).then(res => { // 필터값을 전송하여 게시글 데이터 가져옴
            let data = res.data.data
            for (let v of data.results) {
              v.loading = false
            }
            this.loadingTable = false
            this.articles = data.results // 필터를 거쳐 나온 게시글 데이터
            this.total = data.total
          }).catch(() => {
            this.loadingTable = false
          })
        }
      },
      changeRoute () { // 쿼리값을 변경 후 route 변경
        let query = utils.filterEmptyValue(this.buildQuery())
        let routeName = 'comment-list'
        this.$router.push({
          name: routeName,
          query: utils.filterEmptyValue(query)
        })
      }
    },
    computed: {
      ...mapGetters(['website', 'modalStatus', 'user']),

      previewStyle () {
        return {
          'width': this.preview.w + 'px',
          'height': this.preview.h + 'px',
          'overflow': 'hidden'
        }
      }
    }
  }
</script>

<style lang="less" scoped>

  .flex-container {
    flex-wrap: wrap;
    justify-content: flex-start;
  }
</style>
