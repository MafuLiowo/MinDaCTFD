<template>
  <div class="border-bottom">
    <div>
      <button
        type="button"
        class="close float-right"
        aria-label="Close"
        @click="deleteField()"
      >
        <span aria-hidden="true">&times;</span>
      </button>
    </div>

    <div class="row">
      <div class="col-md-3">
        <div class="form-group">
          <label>字段类型</label>
          <select
            class="form-control custom-select"
            v-model.lazy="field.field_type"
          >
            <option value="text">文字</option>
            <option value="boolean">是否</option>
          </select>
          <small class="form-text text-muted"
            >展示给其他用户的字段类型</small
          >
        </div>
      </div>
      <div class="col-md-9">
        <div class="form-group">
          <label>字段名</label>
          <input type="text" class="form-control" v-model.lazy="field.name" />
          <small class="form-text text-muted">字段名</small>
        </div>
      </div>

      <div class="col-md-12">
        <div class="form-group">
          <label>字段描述</label>
          <input
            type="text"
            class="form-control"
            v-model.lazy="field.description"
          />
          <small id="emailHelp" class="form-text text-muted"
            >字段描述</small
          >
        </div>
      </div>

      <div class="col-md-12">
        <div class="form-check">
          <label class="form-check-label">
            <input
              class="form-check-input"
              type="checkbox"
              v-model.lazy="field.editable"
            />
            在个人资料里是否可更改
          </label>
        </div>
        <div class="form-check">
          <label class="form-check-label">
            <input
              class="form-check-input"
              type="checkbox"
              v-model.lazy="field.required"
            />
            注册时需要填写
          </label>
        </div>
        <div class="form-check">
          <label class="form-check-label">
            <input
              class="form-check-input"
              type="checkbox"
              v-model.lazy="field.public"
            />
            展示在公开资料
          </label>
        </div>
      </div>
    </div>

    <div class="row pb-3">
      <div class="col-md-12">
        <div class="d-block">
          <button
            class="btn btn-sm btn-success btn-outlined float-right"
            type="button"
            @click="saveField()"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CTFd from "../../../compat/CTFd";
import { ezToast } from "../../../compat/ezq";

export default {
  props: {
    index: Number,
    initialField: Object,
  },
  data: function () {
    return {
      field: this.initialField,
    };
  },
  methods: {
    persistedField: function () {
      // We're using Math.random() for unique IDs so new items have IDs < 1
      // Real items will have an ID > 1
      return this.field.id >= 1;
    },
    saveField: function () {
      let body = this.field;
      if (this.persistedField()) {
        CTFd.fetch(`/api/v1/configs/fields/${this.field.id}`, {
          method: "PATCH",
          credentials: "same-origin",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        })
          .then((response) => {
            return response.json();
          })
          .then((response) => {
            if (response.success === true) {
              this.field = response.data;
              ezToast({
                title: "Success",
                body: "Field has been updated!",
                delay: 1000,
              });
            }
          });
      } else {
        CTFd.fetch(`/api/v1/configs/fields`, {
          method: "POST",
          credentials: "same-origin",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        })
          .then((response) => {
            return response.json();
          })
          .then((response) => {
            if (response.success === true) {
              this.field = response.data;
              ezToast({
                title: "Success",
                body: "Field has been created!",
                delay: 1000,
              });
            }
          });
      }
    },
    deleteField: function () {
      if (confirm("Are you sure you'd like to delete this field?")) {
        if (this.persistedField()) {
          CTFd.fetch(`/api/v1/configs/fields/${this.field.id}`, {
            method: "DELETE",
            credentials: "same-origin",
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
            },
          })
            .then((response) => {
              return response.json();
            })
            .then((response) => {
              if (response.success === true) {
                this.$emit("remove-field", this.index);
              }
            });
        } else {
          this.$emit("remove-field", this.index);
        }
      }
    },
  },
};
</script>

<style scoped></style>
