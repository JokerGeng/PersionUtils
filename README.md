# PersionUtils
```C#

﻿using bsttracebackend.Utils;
using Newtonsoft.Json;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq.Expressions;
using System.Reflection;
using System.Text;

namespace GPUProfile.Utils
{
    public class ConverterHelper
    {
        public static TDestination Convert<TDestination>(object source) where TDestination : class, new()
        {
            if (source == null)
            {
                return default;
            }
            Type sourceType = source.GetType();
            TDestination target = new TDestination();
            Type targetType = target.GetType();

            try
            {
                PropertyInfo[] sourceProperties = sourceType.GetProperties();
                PropertyInfo[] targetProperties = targetType.GetProperties();

                foreach (var sourceProperty in sourceProperties)
                {
                    try
                    {
                        PropertyInfo targetProperty = Array.Find(targetProperties, p => p.Name.ToLower() == sourceProperty.Name.ToLower());

                        if (targetProperty != null)
                        {
                            if (IsIsPrimitiveOrString(sourceProperty.PropertyType) && IsIsPrimitiveOrString(targetProperty.PropertyType))
                            {
                                //base type
                                if (targetProperty.CanWrite && targetProperty.PropertyType == sourceProperty.PropertyType)
                                {
                                    object value = sourceProperty.GetValue(source);
                                    if (value != null)
                                    {
                                        targetProperty.SetValue(target, value);
                                    }
                                }
                            }
                            else if (sourceProperty.PropertyType.IsClass && targetProperty.PropertyType.IsClass &&
                                !IsCollectionType(sourceProperty.PropertyType) &&
                                !IsCollectionType(targetProperty.PropertyType))
                            {
                                //user define class ,not collection
                                if (targetProperty.CanWrite)
                                {
                                    var sourceValue = sourceProperty.GetValue(source);
                                    if (sourceValue != null)
                                    {
                                        var convertMethod = typeof(ConverterHelper).GetMethod("Convert").MakeGenericMethod(targetProperty.PropertyType);
                                        var targetValue = convertMethod.Invoke(null, new object[1] { sourceValue });
                                        targetProperty.SetValue(target, targetValue);
                                    }

                                }
                            }
                            else if (IsCollectionType(sourceProperty.PropertyType) && IsCollectionType(targetProperty.PropertyType))//集合
                            {
                                var targetValueType = targetProperty.PropertyType.GetGenericArguments()[0];
                                var sourceValueType = sourceProperty.PropertyType.GetGenericArguments()[0];
                                if (targetValueType.Name != sourceValueType.Name)
                                {
                                    continue;
                                }

                                var sourceCollection = (IList)sourceProperty.GetValue(source);
                                if ((sourceCollection?.Count ?? 0) <= 0)
                                {
                                    continue;
                                }

                                var targetCollection = targetProperty.GetValue(target) as IList;
                                if (IsIsPrimitiveOrString(targetValueType))
                                {
                                    foreach (var sourceElement in sourceCollection)
                                    {
                                        targetCollection.Add(sourceElement);
                                    }
                                }
                                else
                                {
                                    var convertMethod = typeof(ConverterHelper).GetMethod("Convert").MakeGenericMethod(targetValueType);
                                    foreach (var sourceElement in sourceCollection)
                                    {
                                        var targetElement = convertMethod.Invoke(null, new object[1] { sourceElement });
                                        if (targetElement == null)
                                        {
                                            continue;
                                        }
                                        targetCollection.Add(targetElement);
                                    }
                                }
                            }
                        }
                    }
                    catch (Exception ex)
                    {
                        LogUtil.logger.Error("Convert==>" + ex);
                    }
                }
            }
            catch (Exception ex)
            {
                LogUtil.logger.Error("Convert==>" + ex);
            }

            return target;
        }

        internal static IList<TDestination> Convert<TSource, TDestination>(IList<TSource> source) where TDestination : class, new()
        {
            IList<TDestination> result = new List<TDestination>();
            if ((source?.Count ?? 0) > 0)
            {
                foreach (var item in source)
                {
                    var target = Convert<TDestination>(item);
                    result.Add(target);
                }
            }
            return result;
        }

        internal static T Clone<T>(T source)
        {
            if (source is null)
            {
                throw new ArgumentNullException(nameof(source));
            }
            var cStr = JsonConvert.SerializeObject(source);
            var c = JsonConvert.DeserializeObject<T>(cStr);
            return c;
        }

        static bool IsIsPrimitiveOrString(Type obj)
        {
            return obj.IsPrimitive || obj == typeof(string);
        }

        static bool IsCollectionType(Type type)
        {
            return type.IsGenericType && type.GetInterface("IEnumerable") != null;
        }
    }
}


```
