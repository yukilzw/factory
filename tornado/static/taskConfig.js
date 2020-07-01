let moment = window.moment
class TaskConfig extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      title: this.props.drawerTitle,
      visible: this.props.showDrawer,
      selectMaterialAry: [{ id: 0, value: '' }],
      selectData: [],
      adminAct: this.props.admin == 1 ? false : true,
      augeId1: ''
    }
  }

  componentDidMount() {
    this.state.visible && this.fetch() // 请求select数据
    // this.state.visible && this.fetch2()
  }

  fetch = (data) => {
    startRequestByCsrf('/queryAllReachMaterialList', {}, res => {
      let { success, errMsg, data } = res
      if (!success) {
        alert(errMsg)
        return
      } else {
        this.state.title == '编辑任务' && this.fetch2()
        let selectData = data.reduce((acc, it) => {
          it.id && acc.push({ id: it.id, value: it.materialName })
          return acc
        }, [])
        this.setState({ loading: false, selectData })
      }
    })
  }

  fetch2 = () => {
    let url = this.props.type == 'review' ? '/queryReviewTaskDetail' : '/queryReachTaskDetail'
    startRequestByCsrf(url, { taskId: this.props.id }, res => {
      let { success, errMsg, data } = res
      if (!success) {
        alert(errMsg)
        return
      }
      if (data.materialDTOList && data.materialDTOList.length !== 0) {
        let selectMaterialAry = []
        data.materialDTOList && data.materialDTOList.map(it => {
          selectMaterialAry.push({ id: it.id, value: it.materialName })
        })
        this.setState({ selectMaterialAry })
      }
    })
  }

  onClose = (update) => {
    this.props.clearFormData(update)
  }

  handleSubmitForm = () => {
    this.props.form.validateFields((err, values) => {
      // alert(JSON.stringify(values))
      if (!err) {
        let materialListTest = values.materialListTest.reduce((result, it) => {
          if (it.id === 0) {
            return result
          }
          result.push(it)
          return result
        }, [])
        if (materialList == 0) return        // ?????????? length?
        let materialList = materialListTest
        values.startTime = new Date(values.time[0]).getTime().toString()
        values.endTime = new Date(values.time[1]).getTime().toString()
        values.sendTime = new Date(values.sendTime[1]).getTime().toString()
        values.taskType = this.search(values.taskType, true)
        if(values.augeId1) {
          values.augeId = values.augeId1
        }
        if (values.editSendType) {
          values.sendType = values.editSendType;
        }
        delete values.augeId1
        delete values.editSendType
        // alert(JSON.stringify(values))

        let flag = this.state.title == '编辑任务'
        let { id, startTime, endTime, augeId, sendType, launchPeriod, taskName, globalCheck, excludeDau, globalCheck1, excludeDau1, taskType, bizSceneCode } = values
        let data = flag ? { id, augeId, sendType, launchPeriod, taskName, startTime, endTime, materialList, globalCheck, excludeDau, taskType, bizSceneCode }
          : { augeId, sendType, launchPeriod, startTime, endTime, taskName, materialList, globalCheck: globalCheck1, excludeDau: excludeDau1, taskType, bizSceneCode }
        let url = this.props.type == 'review' ? (flag ? 'editReviewTask' : '/addReachTask') : '/editReachTask'
        startRequestByCsrf(url, data, res => {
          if (!res.success) {
            alert(res.errMsg)
            return
          }
          this.onClose('update')
        })
      }
    })
  }

  plus = (selectMaterialAry) => {
    selectMaterialAry.push({ id: new Date().getTime(), value: '' })
    this.setState({ selectMaterialAry })
  }

  minus = (id, selectMaterialAry) => {
    let idx = 0
    for (let i = 0; i < selectMaterialAry.length; i++) {
      if (selectMaterialAry[i].id == id) {
        idx = i
      }
    }
    selectMaterialAry.splice(idx, 1)
    this.setState({ selectMaterialAry })
  }

  handleSelectMaterial = (value, id, selectMaterialAry, idx) => {
    selectMaterialAry[idx] = { id: id.key, value: id.props.children }
    this.setState({ selectMaterialAry })
  }

  search = (val, type) => {
    if(val === '实时') {
      !type && this.setState({augeId1: 1})
      return 2
    } else if(val === '班车') {
      return 1
    } else if(val === '短信(产品)') {
      return 3
    } else if(val === '短信(营销)') {
      return 4
    } else if (val === '定时') {
      return 5;
    }
  }

  changeSendType = (value) => {
    return parseInt(value);
  }

  render() {
    const { getFieldDecorator, getFieldValue } = this.props.form;
    const { selectMaterialAry, selectData, augeId1 } = this.state;
    const {sendType, bizSceneCode} = this.props;
    const dateFormat = 'YYYY.MM.DD hh:mm:ss';
    const disabledDate = (current) => {
      return current && current < moment().startOf('day')
    }
    const formItemLayout = {
      labelCol: {
        span: 5
      },
      wrapperCol: {
        span: 16
      }
    };

    return (
      <div>
        <antd.Drawer
          title={this.state.title}
          width={720}
          placement="right"
          visible={this.state.visible}
          style={{
            height: 'calc(100% - 55px)',
            overflow: 'auto',
            paddingBottom: 53
          }}
          onClose={this.onClose}
        >
          <antd.Form onSubmit={this.handleSubmitForm}>
            {this.state.title == '编辑任务' && <antd.Form.Item {...formItemLayout} label="任务ID">
              {getFieldDecorator('id', {
                rules: [{ required: false }],
              })(<antd.Input placeholder="任务ID" />)}
            </antd.Form.Item>}
            <antd.Form.Item {...formItemLayout} label="任务名称">
              {getFieldDecorator('taskName', {
                rules: [{ required: true }],
              })(<antd.Input placeholder="任务名称" />)}
            </antd.Form.Item>
            <antd.Form.Item {...formItemLayout} label="任务类型">
              {getFieldDecorator('taskType', {
                rules: [{ required: true }],
              })(
                <antd.Select placeholder="实时/班车/短信(产品)/短信(营销)" defaultValue="a3" style={{ width: '350px' }}  onChange={(value) => this.search(value, false)}>
                  <Option value="实时">实时</Option>
                  <Option value="班车">班车</Option>
                  <Option value="短信(产品)">短信(产品)</Option>
                  <Option value="短信(营销)">短信(营销)</Option>
                  <Option value="定时">定时</Option>
                </antd.Select>
              )}
            </antd.Form.Item>
            {
              getFieldValue('taskType') === '定时' && <antd.Form.Item {...formItemLayout} label="发送时间">
                {getFieldDecorator('sendTime', {
                  initialValue: [moment(), moment()],
                  rules: [{ type: 'array', required: true }],
                })(<antd.DatePicker.RangePicker showTime format={dateFormat} disabledDate={disabledDate} />)}
              </antd.Form.Item>
            }
            {
              this.state.title == '编辑任务' ?
              <antd.Form.Item {...formItemLayout} label="关联人群">
                {getFieldDecorator('augeId', {
                  rules: [{ required: false }],
                })(<antd.Input placeholder="奥格人群ID" />)}
              </antd.Form.Item>
              :
              <antd.Form.Item {...formItemLayout} label="关联人群">
                {getFieldDecorator('augeId1', {
                  rules: [{ required: false }],
                  initialValue: augeId1,
                })(<antd.Input placeholder="奥格人群ID" />)}
              </antd.Form.Item>
            }
            <antd.Form.Item {...formItemLayout} label="关联素材">
              {getFieldDecorator('materialListTest', {
                initialValue: selectMaterialAry,
              })(
                <SelectGroup value={selectMaterialAry} plus={this.plus} minus={this.minus}
                  handleSelectMaterial={this.handleSelectMaterial} selectData={selectData} />
              )}
            </antd.Form.Item>
            <antd.Form.Item {...formItemLayout} label="有效期">
              {getFieldDecorator('time', {
                initialValue: [moment(), moment()],
                rules: [{ type: 'array', required: true }],
              })(<antd.DatePicker.RangePicker showTime format={dateFormat} disabledDate={disabledDate} />)}
            </antd.Form.Item>
            <antd.Form.Item {...formItemLayout} label="发送类型">
              {getFieldDecorator('editSendType', {
                rules: [{ required: true }],
                initialValue: sendType !== undefined ? `${sendType}` : ''
              })(<antd.Select placeholder="请选择发送类型" onChange={(value) => this.changeSendType(value)}>
                <Option value='0'>[PUSH+SAVE]每日捡漏</Option>
                <Option value='1'>[PUSH+SAVE]速卖指南</Option>
                <Option value='2'>[PUSH+SAVE]通知消息</Option>
                <Option value='3'>[PUSH+SAVE]IM消息</Option>
              </antd.Select>)}
            </antd.Form.Item>
            <antd.Form.Item {...formItemLayout} label="业务场景">
              {getFieldDecorator('bizSceneCode', {
                rules: [{ required: true }],
                initialValue: bizSceneCode
              })(<antd.Select showSearch placeholder="请选择业务场景">
                <Option value='act'>营销消息</Option>
                <Option value='pre84'>IM消息</Option>
                <Option value='pre96'>订单消息</Option>
                <Option value='pre213'>内容更新消息</Option>
              </antd.Select>)}
            </antd.Form.Item>
            <antd.Form.Item {...formItemLayout} label="任务疲劳度" disabled={this.state.adminAct}>
              {getFieldDecorator('launchPeriod', {
                rules: [{ required: true }],
              })(<antd.InputNumber style={{ width: 60, marginRight: 10 }} />)}
              天 默认为7天，可联系管理员修改
            </antd.Form.Item>
            {
              this.state.title == '编辑任务' ?
              <div>
                <antd.Form.Item {...formItemLayout} label="可选配置">
                  {getFieldDecorator('globalCheck', {
                    rules: [{ required: false }],
                    valuePropName: 'checked',
                    initialValue: true,
                  })(<antd.Checkbox defaultChecked>全局优化</antd.Checkbox>)}
                  默认全局优化，可联系管理员修改
                </antd.Form.Item>
                <antd.Form.Item {...formItemLayout} label="排除日活">
                  {getFieldDecorator('excludeDau', {
                    rules: [{ required: false }],
                    valuePropName: 'checked',
                    initialValue: true,
                  })(<antd.Checkbox defaultChecked>排除日活</antd.Checkbox>)}
                  默认排除日活，可联系管理员修改
                </antd.Form.Item>
              </div> 
              :
              <div>
                <antd.Form.Item {...formItemLayout} label="可选配置">
                  {getFieldDecorator('globalCheck1', {
                    rules: [{ required: false }],
                    valuePropName: 'checked',
                    initialValue: true,
                  })(<antd.Checkbox defaultChecked disabled={this.state.adminAct}>全局优化</antd.Checkbox>)}
                  默认全局优化，可联系管理员修改
                </antd.Form.Item>
                <antd.Form.Item {...formItemLayout} label="排除日活">
                  {getFieldDecorator('excludeDau1', {
                    rules: [{ required: false }],
                    valuePropName: 'checked',
                    initialValue: true,
                  })(<antd.Checkbox defaultChecked disabled={this.state.adminAct}>排除日活</antd.Checkbox>)}
                  默认排除日活，可联系管理员修改
                </antd.Form.Item>
              </div>
            }
            
            <div
              style={{
                position: 'absolute',
                bottom: 0,
                width: '100%',
                borderTop: '1px solid #e8e8e8',
                padding: '10px 16px',
                textAlign: 'right',
                left: 0,
                background: '#fff',
                borderRadius: '0 0 4px 4px',
              }}
            >
              <antd.Button onClick={this.onClose} style={{ marginRight: 8 }}>取消</antd.Button>
              <antd.Button type="primary" htmlType="submit" >完成</antd.Button>
            </div>
          </antd.Form>
        </antd.Drawer>
      </div>
    );
  }
}


class SelectGroup extends React.Component {

  getMaterial = () => {
    return this.props.selectData.map(this.renderOption)
  }

  renderOption = (entry, idx) => {
    return (
      <antd.Select.Option value={entry.id} key={entry.id}>{entry.value}</antd.Select.Option>
    )
  }

  handleSelectMaterial = (value, id, idx) => {
    this.props.handleSelectMaterial(value, id, this.props.value, idx)
  }
  plus = () => {
    this.props.plus(this.props.value)
  }
  minus = (id) => {
    this.props.minus(id, this.props.value)
  }

  render() {
    return (
      <div>
        {this.props.value && this.props.value.map((material, idx) => {
          return <div key={material.id} style={{ display: 'flex', alignItems: 'center', marginBottom: 14 }}>
            <antd.Select showSearch placeholder="可关联一个或多个" style={{ marginRight: 14 }} value={material.value}
              onChange={(value, id) => this.handleSelectMaterial(value, id, idx)}
              filterOption={(input, option) =>
                option.props.children.toString().indexOf(input) >= 0
              }>
              {this.getMaterial()}
            </antd.Select>
            {idx != 0 ? <antd.Icon type='minus-circle' onClick={() => this.minus(material.id)} style={{ fontSize: 24, color: '#ccc' }} />
              :
                <div>
                  <antd.Icon type='plus-circle' onClick={this.plus} style={{ fontSize: 24, color: '#ccc' }} />
                  <antd.Icon type='minus-circle' onClick={() => this.minus(material.id)} style={{ fontSize: 24, color: '#ccc' }} />
                </div>
            }
          </div>
        })}
      </div>
    )
  }
}
