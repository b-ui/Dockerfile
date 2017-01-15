from app.common.log_util import logger


class ContainerTag(object):
    def __init__(self, name, content={}, required=False, many=False, skip=False, parent_name='root'):
        self.name = name
        self.required = required
        self.parent_name = parent_name
        self.content = content
        self.many = many
        self.skip = skip


class VField(object):
    def __init__(self, name, required=False, default=None, parent_name='root', allow_none=None,
                 data_type='string', length=20):
        self.name = name
        self.required = required
        self.allow_none = allow_none
        self.data_type = data_type
        self.length = length
        self.default = default


class VNullField(VField):
    pass


class VGlobalField(VField):
    def push_field_value_to_global(self, source_field_name, source_field_value, variables):
        variables.update({source_field_name: source_field_value})


class VFunctionField(VField):
    def __init__(self, name, mapping_function, reverse_mapping_function, required=True):
        if mapping_function and not callable(mapping_function):
            raise ValueError('Object {0!r} is not callable.'.format(mapping_function))
        if reverse_mapping_function and not callable(reverse_mapping_function):
            raise ValueError('Object {0!r} is not callable.'.format(reverse_mapping_function))
        self.name = name
        self.trans_function = mapping_function
        self.reverse_function = reverse_mapping_function
        self.required = required
        self.default = ''

    #         super(VFunctionField, self).__init__(name)

    def transform(self, input_obj, output_obj, output_field_name, input_field):
        self.trans_function(input_obj, output_obj, output_field_name, input_field)

    def reverse_transform(self, input_obj, output_obj, input_field, var_fields):
        self.reverse_function(output_obj, input_field)


class VReferenceField(VFunctionField):
    def __init__(self, name, mapping_function, reverse_mapping_function):
        super(VReferenceField, self).__init__(name, mapping_function, reverse_mapping_function)
        self.required = False
        self.default = None

    def transform(self, input_obj, output_obj, input_field_name, output_field_name, variables):
        self.trans_function(input_obj, output_obj, input_field_name, output_field_name, variables)

    def reverse_transform(self, input_obj, output_obj, input_field, variables):
        self.reverse_function(output_obj, input_field, variables)


class VDictSchema(object):
    def __init__(self, dict_schema):
        self.schema = dict_schema
        self.vars = {}

    def __mapping_field(self, in_data, out_data, origin_name, to_field):
        errors = []
        data = in_data.get(origin_name) if isinstance(in_data, dict) else None

        if data is None and to_field.required:
            errors.append('{0} is required,but absent'.format(origin_name))
        elif data is None:
            if isinstance(to_field, VField) and not to_field.required \
                    and to_field.default is not None:
                out_data[to_field.name] = to_field.default
            elif isinstance(to_field, VReferenceField):
                error = to_field.transform(in_data, out_data, origin_name, to_field.name, self.vars)
                if error:
                    errors.append(error)
            else:
                pass
        # data is not None
        else:
            if isinstance(to_field, ContainerTag):
                return_errors = self.__mapping_fields(
                    to_field.content, in_data[origin_name], out_data)
                if len(return_errors) > 0:
                    errors.extend(return_errors)
            elif isinstance(to_field, VReferenceField):
                out_data[to_field.name] = data
            elif isinstance(to_field, VFunctionField):
                error = to_field.transform(in_data, out_data, to_field.name, in_data[origin_name])
                if error:
                    errors.append(error)
            elif isinstance(to_field, VGlobalField):
                to_field.push_field_value_to_global(origin_name, in_data[origin_name], self.vars)
                out_data[to_field.name] = data
            elif isinstance(to_field, VNullField):
                pass
            else:
                out_data[to_field.name] = data

        return errors

    def __mapping_fields(self, schema, in_data, out_data):
        errors = []

        for k, v in schema.items():
            return_errors = []
            if not isinstance(v, ContainerTag):
                # print '--------element----{0}'.format(in_data)
                return_errors.extend(self.__mapping_field(in_data, out_data, k, v))
            else:
                if not v.many:
                    child = in_data
                    if not v.skip:
                        out_data[v.name] = {}
                        return_errors.extend(self.__mapping_field(child, out_data[v.name], k, v))
                    else:
                        return_errors.extend(self.__mapping_field(child, out_data, k, v))
                        # 向下取两层, 进行数据展开
                else:
                    childs = in_data[k]
                    if not isinstance(childs, list):
                        childs = [childs]
                    # print '--------childs----{0}'.format(childs)
                    lines = []
                    if v.skip:
                        for item in childs:
                            temp_errors = self.__mapping_fields(v.content, item, out_data)
                    else:
                        out_data[v.name] = lines
                        for item in childs:
                            line = {}
                            lines.append(line)
                            # __mapping_field(item, line, k , v)
                            temp_errors = self.__mapping_fields(v.content, item, line)
                    if len(temp_errors) > 0:
                        return_errors.extend(temp_errors)

            if len(return_errors) > 0:
                errors.extend(return_errors)
        return errors

    def dict_mapping(self, in_data):
        out_data = {}
        errors = []

        for k, v in self.schema.items():
            errors.extend(self.__mapping_field(in_data, out_data, k, v))

        logger.info('out_data = {}'.format(str(out_data)))
        logger.info('errors = {}'.format(str(errors)))
        return out_data, errors

    def __reverse_mapping_field(self, in_data, out_data, origin_name, to_field):
        errors = []

        # input data field
        if isinstance(to_field, ContainerTag):
            node = {}
            out_data[origin_name] = node
            return_errors = self.__reverse_mapping_fields(
                to_field.content, in_data, node)
            if len(return_errors) > 0:
                errors.extend(return_errors)
        else:
            data = in_data.get(to_field.name) if isinstance(
                in_data, dict) else None
            # print '--------to_field----{0}'.format(to_field.name)
            # print '--------data0----{0}'.format(data)

            if data is not None and not isinstance(data, dict):
                out_data[origin_name] = data
                # print '--------data1----{0}'.format(data)
            elif data is None and to_field.required:
                errors.append('{0} is required,but absent'.format(to_field.name))
            elif data and isinstance(data, dict):
                errors.append('{0} should be simple field,but it is dict'.format(to_field.name))
            else:
                pass
                logger.debug('--------else----{0}'.format(data))

        return errors

    def __reverse_mapping_fields(self, schema, in_data, out_data):
        errors = []

        for k, v in schema.items():
            return_errors = []
            if not isinstance(v, ContainerTag):
                return_errors.extend(self.__reverse_mapping_field(
                    in_data, out_data, k, v))

            else:
                if not v.many:
                    return_errors.extend(self.__reverse_mapping_field(in_data,
                                                                      out_data, k, v))
                    # todo 如果k是可选节点，需要根据子字段的取值来确定是否
                    # 有这个字段，则需要在此处删除掉这个节点
                else:  # 向下取两层, 进行数据展开
                    nodes = []
                    out_data[k] = nodes
                    print('in_data===={0}'.format(in_data))
                    lines = in_data[v.name]
                    if not isinstance(lines, list):
                        errors.append('{0} should be list'.format(v.name))
                        return errors

                    for line in lines:
                        item = {}
                        nodes.append(item)
                        temp_errors = []
                        temp_errors.extend(self.__reverse_mapping_fields(v.content,
                                                                         line, item))
                        if len(temp_errors) > 0:
                            return_errors.extend(temp_errors)

            if len(return_errors) > 0:
                errors.extend(return_errors)
        return errors

    def reverse_dict_mapping(self, in_data):
        out_data = {}
        errors = []

        for k, v in self.schema.items():
            errors.extend(self.__reverse_mapping_field(in_data, out_data, k, v))

        logger.debug('reverse errors =' + str(errors))
        logger.debug('out_data =' + str(out_data))
        return out_data, errors

    def dict_validate(self, in_data):
        errors = None
        return True, errors
