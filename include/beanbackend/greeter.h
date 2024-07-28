#pragma once

#include <string>

namespace greeter
{

  /**  Language codes to be used with the Greeter class */
  enum class LanguageCode
  {
    EN,
    DE,
    ES,
    FR
  };

  /**
   * A class documentation.
   */
  class Greeter
  {
    std::string name;

   public:
     /**
      * @brief A method description.this goes on for mul
      * tiple lines.
      *
      * A more detailed description.
      *
      * @param name A param description.
      */
    explicit Greeter(std::string name);

    /**
     * @brief Creates a localized string containing the greeting
     * @param lang the language to greet in
     * @return a string containing the greeting
     */
    std::string greet(LanguageCode lang = LanguageCode::EN) const;
  };

}  // namespace greeter
