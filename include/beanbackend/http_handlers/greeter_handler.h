#pragma once

#include <string_view>
#include <userver/components/component_list.hpp>
#include <userver/server/handlers/http_handler_base.hpp>

#include "userver/server/http/http_request.hpp"
#include "userver/server/request/request_context.hpp"

namespace greeter
{
  /**
   * Exposes the '/greet' endpoint.
   */
  class GreeterHandler final : public userver::server::handlers::HttpHandlerBase
  {
   public:
    /**
     * Name of the handler.
     */
    static constexpr std::string_view kName = "handler-greeter";

    using userver::server::handlers::HttpHandlerBase::HttpHandlerBase;

    /**
     * The handler.
     * @param request The request
     * @return The response
     */
    std::string HandleRequestThrow(
        const userver::server::http::HttpRequest &request,
        userver::server::request::RequestContext & /* request_context */) const override;
  };
};  // namespace greeter
