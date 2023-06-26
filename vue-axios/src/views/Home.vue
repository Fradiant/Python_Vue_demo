<template>
  <div class="home">
    <h1>前后端分离小demo</h1>

    <!-- 表格区域 -->
    <el-table
      :data="table"
      stripe
      :cell-style="{ textAlign: 'center' }"
      :header-cell-style="{ textAlign: 'center' }"
    >
      <el-table-column prop="id" label="ID" width="100" sortable />
      <el-table-column prop="name" label="姓名">
        <template slot-scope="scope">
          <el-tag type="info" effect="plain">{{ scope.row.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="age" label="年龄" />
      <el-table-column prop="sex" label="性别" />

      <el-table-column label="操作" width="210">
        <template slot="header">
          <span class="op">操作</span>
          <el-button size="mini" class="add" @click="add" icon="el-icon-plus"
            >添加一条记录</el-button
          >
        </template>
        <template slot-scope="scope">
          <el-button
            type="info"
            size="mini"
            @click="handEdit(scope.$index, scope.row)"
            icon="el-icon-edit"
            round
            >编辑</el-button
          >
          <el-popconfirm
            title="确认删除吗？"
            @confirm="handDelete(scope.$index, scope.row)"
          >
            <el-button
              type="danger"
              size="mini"
              icon="el-icon-delete"
              round
              slot="reference"
              >删除</el-button
            >
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <!-- 弹出窗 -->
    <el-dialog
      :title="title"
      :visible="dialogVisible"
      width="30%"
      :before-close="handleClose"
    >
      <el-form
        :model="form"
        status-icon
        :rules="rules"
        ref="form"
        label-width="60px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" autocomplete="off" />
        </el-form-item>
        <el-form-item label="年龄" prop="age">
          <el-input
            type="number"
            min="1"
            max="99"
            v-model="form.age"
            autocomplete="off"
          />
        </el-form-item>
        <el-form-item label="性别" prop="sex">
          <el-radio-group v-model="form.sex">
            <el-radio label="男"></el-radio>
            <el-radio label="女"></el-radio>
            <el-radio label="未知"></el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="reset">重置</el-button>
        <el-button type="primary" @click="save">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>

export default {
  name: 'Home',
  data() {
    // 自定义验证规则
    var validateAge = (rule, value, callback) => {
      if (value === '' || value === undefined) {
        callback(new Error('请输入年龄'))
      } else if (isNaN(value)) {
        callback(new Error('请输入数字'))
      } else if (value < 1 || value > 100) {
        callback(new Error('年龄必须在1~100之间'))
      } else {
        callback()
      }
    }
    return {
      table: [],
      dialogVisible: false,
      title: '',
      form: {},
      rules: {
        name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
        age: [{ required: true, validator: validateAge, trigger: 'blur' }],
        sex: [{ required: true, message: '请选择性别', trigger: 'blur' }],
      }
    }
  },
  created() {
    this.init()
  },
  methods: {
    init() {
      this.$axios.get('/all').then(res => {
        // console.log(res);
        if (res.code == 200)
          this.table = res.data
      })
    },
    add() {
      this.dialogVisible = true
      this.title = '添加记录'
      this.form = {}
    },
    handEdit(index, row) {
      // console.log(row);
      this.dialogVisible = true
      this.title = '编辑记录'
      this.form = JSON.parse(JSON.stringify(row))
    },
    handDelete(index, row) {
      // console.log(row);
      let id = JSON.parse(JSON.stringify(row)).id
      this.$axios.delete(`/delete?id=${id}`).then(res => {
        if (res.code == 200) {
          this.$notify.success({
            title: '成功',
            message: res.msg,
            duration: 2000
          })
          this.init()
        } else {
          this.$notify.success({
            title: '失败',
            message: res.msg,
            duration: 2000
          })
        }
      })
    },
    handleClose() {
      this.dialogVisible = false
      this.init()
    },
    reset() {
      let id = undefined
      if ('id' in this.form) {
        id = this.form.id
      }
      this.form = {}
      if (id != undefined) this.form.id = id
    },
    save() {
      this.$refs['form'].validate(valid => {    // 判断是否通过验证
        if (valid) {
          console.log(this.form);
          if ('id' in this.form) {
            // console.log('修改');

            this.$axios.put('/update', this.form).then(res => {
              if (res.code == 200) {
                let _this = this
                this.$notify.success({
                  title: '成功',
                  message: res.msg,
                  duration: 2000,
                  onClose: () => _this.handleClose()
                });
              } else {
                this.$notify.error({
                  title: '错误',
                  message: res.msg,
                  duration: 2000
                });
              }
            })

          } else {
            // console.log('添加');

            this.$axios.post('/add', this.form).then(res => {
              if (res.code == 200) {
                let _this = this
                this.$notify.success({
                  title: '成功',
                  message: res.msg,
                  duration: 2000,
                  onClose: () => _this.handleClose()
                });
              } else {
                this.$notify.error({
                  title: '错误',
                  message: res.msg,
                  duration: 2000
                });
              }
            })
          }
        }
      })
    }
  }
}
</script>

<style>
h1 {
  text-align: center;
  margin: 50px 0;
}
.el-table {
  width: 60% !important;
  margin: 0 auto;
}
.el-button {
  margin: 0 5px;
}
span.op {
  display: inline-block;
  margin-left: 6px;
}
.el-dialog__body {
  padding-bottom: 0;
}
</style>
