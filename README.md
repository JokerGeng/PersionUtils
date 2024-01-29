# PersionUtils

using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq.Expressions;
using System.Reflection;
using System.Text;

namespace GPUProfile.Models
{
    public class ConverterHelper
    {
        public static TDestination Convert<TDestination>(object source) where TDestination : class, new()
        {
            Type sourceType = source.GetType();
            TDestination target = new TDestination();
            Type targetType = target.GetType();

            try
            {
                PropertyInfo[] sourceProperties = sourceType.GetProperties();
                PropertyInfo[] targetProperties = targetType.GetProperties();

                foreach (var sourceProperty in sourceProperties)
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
                                targetProperty.SetValue(target, value);
                            }
                        }
                        else if (sourceProperty.PropertyType.IsClass && targetProperty.PropertyType.IsClass &&
                            !IsCollectionType(sourceProperty.PropertyType) &&
                            !IsCollectionType(targetProperty.PropertyType))
                        {
                            //user define class ,not collection
                            if(targetProperty.CanWrite)
                            {
                                var sourceValue = sourceProperty.GetValue(source);
                                var convertMethod = typeof(ConverterHelper).GetMethod("Convert").MakeGenericMethod(targetProperty.PropertyType);
                                var targetValue = convertMethod.Invoke(null, new object[1] { sourceValue });
                                targetProperty.SetValue(target, targetValue);
                            }
                        }
                        else if (IsCollectionType(sourceProperty.PropertyType)&& IsCollectionType(targetProperty.PropertyType))//集合
                        {
                            // Handle collection properties
                            var sourceCollection = (IEnumerable)sourceProperty.GetValue(source);
                            var targetTypeOfElements = targetProperty.PropertyType.GetGenericArguments()[0];

                            // Create an empty collection of the target type
                            var targetCollection = (IList)Activator.CreateInstance(typeof(List<>).MakeGenericType(targetTypeOfElements));
                            var convertMethod = typeof(ConverterHelper).GetMethod("Convert").MakeGenericMethod(targetTypeOfElements);
                            foreach (var sourceElement in sourceCollection)
                            {
                                var targetElement = convertMethod.Invoke(null, new object[1] { sourceElement });
                                targetCollection.Add(targetElement);
                                if(!targetProperty.CanWrite)
                                {
                                    //readonly proprety
                                    var readOnlyCollection = targetProperty.GetValue(target) as IList;
                                    readOnlyCollection.Add(targetElement);
                                }
                            }
                            var tt = targetProperty.GetValue(target);
                            if (targetProperty.CanWrite)
                            {
                                targetProperty.SetValue(target, targetCollection);
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }

            return target;
        }

        internal static IList<TDestination> Convert<TSource, TDestination>(IList<TSource> source) where TDestination : class, new()
        {
            IList<TDestination> result = new List<TDestination>();
            foreach (var item in source)
            {
                var target = Convert<TDestination>(item);
                result.Add(target);
            }
            return result;
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
